import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from middleware.analysis import tweet_provider
from sklearn.naive_bayes import MultinomialNB

provider = tweet_provider.TweetProvider()
df_tweets = pd.read_csv("./src/data/Tweets.csv")
df_tweets.dropna(inplace=True)
X_train = df_tweets["text"].tolist()
y_train = df_tweets["sentiment"].tolist()
X_test = provider.get_corpus(30)

tfidf = TfidfVectorizer(use_idf=True, stop_words="english", lowercase=True, strip_accents="ascii",
                        min_df=10, encoding="latin-1", max_features=10000, ngram_range=(1, 2))
X_train = tfidf.fit_transform(X_train)
X_test_transformed = tfidf.transform(X_test)
clf = MultinomialNB()
clf.fit(X_train, y_train)

i = 0
for tweet in X_test:
    print(tweet)
    print(clf.predict(X_test_transformed[i]))
    print("-----")
    i += 1