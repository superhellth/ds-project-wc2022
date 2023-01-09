"""Tool to annotate tweets. Always try to use one from match specific/word cup specific/football related one from "joke/meme"/personal comment/political comment.
Those 2 categories go well together. spam/scam, unrelated and unclassifiable can be used alone. The neutral sentiment is selected if neither positive nor negative is selected."""

import tkinter as tk
import pandas as pd
from middleware.analysis import tweet_provider

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
    """Load tweets from ES"""
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
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
x_offset = (screen_width - WINDOW_WIDTH) // 2
y_offset = (screen_height - WINDOW_HEIGHT) // 2

# Set the window size and position
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x_offset}+{y_offset}")
window.title("Tweet Classification")

current_tweet_index = 0
current_tweet = tweets[current_tweet_index]

CENTER_COLUMN = 2
START_ROW = 0

PLACEHOLDER_TEXT = "\t\t\t\t\t\t\t\t\t\t\t"
bottom_left = tk.Label(master=window, text=PLACEHOLDER_TEXT)
bottom_right = tk.Label(master=window, text=PLACEHOLDER_TEXT)
bottom_left.grid(row=0, column=0)
bottom_right.grid(row=0, column=4)

classified_label = tk.Label(master=window, text="Classified: 0")
classified_label.grid(row=15, column=CENTER_COLUMN)
tweet_label = tk.Label(master=window, text="Tweet Text:")
tweet_label.grid(row=START_ROW, column=CENTER_COLUMN)
tweet_text = tk.Label(master=window, text=current_tweet.get_text())
tweet_text.grid(row=START_ROW + 2, column=0, columnspan=5)
label_label = tk.Label(master=window, text="\nCurrent Labels: ")
label_label.grid(row=START_ROW + 3, column=0, columnspan=5)

current_labels = []


def toggle_label(label):
    """Toggle label for this tweet."""
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

label_button_dict["positive"].grid(row=START_ROW + 4, column=CENTER_COLUMN - 1)
label_button_dict["negative"].grid(row=START_ROW + 4, column=CENTER_COLUMN + 1)
label_button_dict["match specific"].grid(
    row=START_ROW + 5, column=CENTER_COLUMN - 1)
label_button_dict["world cup specific"].grid(
    row=START_ROW + 5, column=CENTER_COLUMN)
label_button_dict["football related"].grid(
    row=START_ROW + 5, column=CENTER_COLUMN + 1)
label_button_dict["personal comment"].grid(
    row=START_ROW + 6, column=CENTER_COLUMN - 1)
label_button_dict["joke/meme"].grid(row=START_ROW + 6, column=CENTER_COLUMN)
label_button_dict["political comment"].grid(
    row=START_ROW + 6, column=CENTER_COLUMN + 1)
label_button_dict["prediction"].grid(
    row=START_ROW + 7, column=CENTER_COLUMN - 1)
label_button_dict["announcement"].grid(row=START_ROW + 7, column=CENTER_COLUMN)
label_button_dict["news"].grid(row=START_ROW + 7, column=CENTER_COLUMN + 1)
label_button_dict["unrelated"].grid(
    row=START_ROW + 8, column=CENTER_COLUMN - 1)
label_button_dict["spam/scam"].grid(row=START_ROW + 8, column=CENTER_COLUMN)
label_button_dict["unclassifiable"].grid(
    row=START_ROW + 8, column=CENTER_COLUMN + 1)
next_button = tk.Button(
    master=window, text="Space/Enter: Next Tweet", command=classify_tweet)
next_button.grid(row=START_ROW + 9, column=CENTER_COLUMN)
window.bind("<space>", classify_tweet)
window.bind("<Return>", classify_tweet)
clear_button = tk.Button(master=window, text="Backspace: Remove label",
                         command=lambda event: toggle_label(current_labels[len(current_labels) - 1]))
clear_button.grid(row=START_ROW + 10, column=CENTER_COLUMN)
window.bind("<BackSpace>", lambda event: toggle_label(
    current_labels[len(current_labels) - 1]))

window.mainloop()
