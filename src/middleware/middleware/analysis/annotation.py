import pandas as pd
from middleware.analysis import tweet_provider
import tkinter as tk

provider = tweet_provider.TweetProvider()
LABELS = {"a": "match announcement", "r": "result related",
          "c": "match commentary", "p": "political", "n": "news", "s": "spam", "o": "other"}
df_class = pd.read_csv("./src/data/classification.csv")
tweets = []
classified = 0


def load_more_tweets():
    global tweets
    num_classified = len(df_class["tweet_id"].tolist())
    tweets += provider.get_tweet_list(size=100, body={"from": num_classified, "query": {"match_all": {}}, "sort": {"author.username": "asc"}})


load_more_tweets()

# GUI
window = tk.Tk()
# Get the screen width and height
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate the position of the window
window_width = 600
window_height = 400
x_offset = (screen_width - window_width) // 2
y_offset = (screen_height - window_height) // 2

# Set the window size and position
window.geometry(f"{window_width}x{window_height}+{x_offset}+{y_offset}")
window.title("Tweet Classification")

current_tweet_index = 0
current_tweet = tweets[current_tweet_index]

classified_label = tk.Label(master=window, text="Classified: 0")
classified_label.pack()
tweet_label = tk.Label(master=window, text="Tweet Text:")
tweet_label.pack()
tweet_text = tk.Label(master=window, text=current_tweet.get_text())
tweet_text.pack()


def classify_tweet(label):
    global current_tweet_index
    global current_tweet
    global classified_label
    global tweets
    global classified
    global window

    last_index = df_class.last_valid_index()
    if last_index is None:
        last_index = 0
    else:
        last_index = last_index + 1
    df_class.loc[last_index] = pd.Series(
        {"tweet_id": current_tweet.get_id(), "label": label})
    df_class.to_csv("./src/data/classification.csv", sep=",",
                    columns=["tweet_id", "label"], index=False)

    current_tweet_index += 1
    # load more tweets if necassary
    if current_tweet_index >= len(tweets):
        load_more_tweets()
    current_tweet = tweets[current_tweet_index]
    tweet_text.config(text=current_tweet.get_text())
    classified += 1
    classified_label.config(text="Classified: " + str(classified))


for label_id, label_text in LABELS.items():
    def make_lambda(label):
        return lambda event=None: classify_tweet(label=label)
    window.bind(str(label_id), make_lambda(label_text))
    button = tk.Button(master=window, text=str(label_id) +
                       ": " + label_text, command=make_lambda(label_text))
    button.pack()

window.mainloop()

# print("Start classifying...")
# print(f"Labels: {LABELS}")
# for tweet in tweets:
#     print(tweet.get_text())
#     label_index = input()
#     label = LABELS[int(label_index)]
#     last_index = df_class.last_valid_index()
#     if last_index is None:
#         last_index = 0
#     else:
#         last_index = last_index + 1
#     df_class.loc[last_index] = pd.Series({"tweet_id": tweet.get_id(), "label": label})

# df_class.to_csv("./src/data/classification.csv", sep=",", columns=["tweet_id", "label"], index=False)
