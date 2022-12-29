import pandas as pd
from middleware.analysis import tweet_provider
import tkinter as tk

provider = tweet_provider.TweetProvider()
LABELS = {"a": "positive", "z": "negative", "b": "neutral",
          "m": "match specific", "w": "world cup specific", "f": "football related",
          "j": "joke/meme", "c": "personal comment", "p": "political comment",
          "d": "prediction", "n": "news", "g": "announcement",
          "s": "spam/scam",
          "u": "unrelated",
          "-": "unclassifiable"}
df_class = pd.read_csv("./src/data/classification.csv")
tweets = []
classified = 0


def load_more_tweets():
    global tweets
    num_classified = len(df_class["tweet_id"].tolist())
    tweets += provider.get_tweet_list(size=300, body={"from": num_classified, "query": {
                                      "match_all": {}}, "sort": {"author.username": "asc"}})


load_more_tweets()

# GUI
window = tk.Tk()
window.columnconfigure(2, weight=1)

# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position of the window
window_width = 1920
window_height = 1080
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
window.title("Tweet Classification")

current_tweet_index = 0
current_tweet = tweets[current_tweet_index]

center_column = 2
start_row = 0

placeholder_text = "\t\t\t\t\t\t\t\t\t\t\t"
bottom_left = tk.Label(master=window, text=placeholder_text)
bottom_right = tk.Label(master=window, text=placeholder_text)
bottom_left.grid(row=0, column=0)
bottom_right.grid(row=0, column=4)

classified_label = tk.Label(master=window, text="Classified: 0")
classified_label.grid(row=15, column=center_column)
tweet_label = tk.Label(master=window, text="Tweet Text:")
tweet_label.grid(row=start_row, column=center_column)
tweet_text = tk.Label(master=window, text=current_tweet.get_text())
tweet_text.grid(row=start_row + 2, column=0, columnspan=5)
label_label = tk.Label(master=window, text="\nCurrent Labels: ")
label_label.grid(row=start_row + 3, column=0, columnspan=5)

current_labels = []


def toggle_label(label):
    global current_labels
    if label in current_labels:
        current_labels.remove(label)
    else:
        current_labels.append(label)
    label_text = "\nCurrent Labels: "
    label_text += ", ".join(current_labels)
    label_label.config(text=label_text)


def classify_tweet(event):
    global current_tweet_index
    global current_tweet
    global classified_label
    global tweets
    global classified
    global window
    global current_labels
    global label_label

    last_index = df_class.last_valid_index()
    if last_index is None:
        last_index = 0
    else:
        last_index = last_index + 1
    
    if "negative" in current_labels:
        sentiment = "negative"
    elif "positive" in current_labels:
        sentiment = "positive"
    else:
        sentiment = "neutral"
    if sentiment in current_labels:
        current_labels.remove(sentiment)
    df_class.loc[last_index] = pd.Series(
        {"tweet_id": current_tweet.get_id(), "labels": current_labels, "sentiment": sentiment})
    df_class.to_csv("./src/data/classification.csv", sep=",",
                    columns=["tweet_id", "labels", "sentiment"], index=False)

    current_tweet_index += 1
    # load more tweets if necassary
    if current_tweet_index >= len(tweets):
        load_more_tweets()
    current_tweet = tweets[current_tweet_index]
    tweet_text.config(text=current_tweet.get_text())
    classified += 1
    classified_label.config(text="Classified: " + str(classified))
    current_labels = []
    label_label.config(text="\nCurrent Labels: ")


label_button_dict = dict()
for label_id, label_text in LABELS.items():
    def make_lambda(label):
        return lambda event=None: toggle_label(label)
    window.bind(str(label_id), make_lambda(label_text))
    button = tk.Button(master=window, text=str(label_id) +
                       ": " + label_text, command=make_lambda(label_text))
    label_button_dict[label_text] = button

label_button_dict["positive"].grid(row=start_row + 4, column=center_column - 1)
label_button_dict["negative"].grid(row=start_row + 4, column=center_column + 1)
label_button_dict["match specific"].grid(
    row=start_row + 5, column=center_column - 1)
label_button_dict["world cup specific"].grid(
    row=start_row + 5, column=center_column)
label_button_dict["football related"].grid(
    row=start_row + 5, column=center_column + 1)
label_button_dict["personal comment"].grid(
    row=start_row + 6, column=center_column - 1)
label_button_dict["joke/meme"].grid(row=start_row + 6, column=center_column)
label_button_dict["political comment"].grid(
    row=start_row + 6, column=center_column + 1)
label_button_dict["prediction"].grid(
    row=start_row + 7, column=center_column - 1)
label_button_dict["announcement"].grid(row=start_row + 7, column=center_column)
label_button_dict["news"].grid(row=start_row + 7, column=center_column + 1)
label_button_dict["unrelated"].grid(
    row=start_row + 8, column=center_column - 1)
label_button_dict["spam/scam"].grid(row=start_row + 8, column=center_column)
label_button_dict["unclassifiable"].grid(
    row=start_row + 8, column=center_column + 1)
next_button = tk.Button(
    master=window, text="Space/Enter: Next Tweet", command=classify_tweet)
next_button.grid(row=start_row + 9, column=center_column)
window.bind("<space>", classify_tweet)
window.bind("<Return>", classify_tweet)
clear_button = tk.Button(master=window, text="Backspace: Remove label",
                         command=lambda event: toggle_label(current_labels[len(current_labels) - 1]))
clear_button.grid(row=start_row + 10, column=center_column)
window.bind("<BackSpace>", lambda event: toggle_label(
    current_labels[len(current_labels) - 1]))

window.mainloop()
