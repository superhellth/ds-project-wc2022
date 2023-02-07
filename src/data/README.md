# Data Files

- Tweets.csv: This file contains sentiment analysis training data. Source: https://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset
  - Tweets_train.csv: Our training split of the file
  - Tweets_test.csv: Our test split of the file
 - classification.csv: This file contains classifier training data. We created it ourselves by annotating ~1000 of our own Tweets with a multi-label system. Each Tweet (only represented by it's ID) has a sentiment (positive, neutral, negative) and one or more of the following labels: "match specific", "world cup specific", "football related", "joke/meme", "personal comment", "political comment", "prediction", "news", "announcement", "spam/scam", "unrelated", "unclassifiable"
 - mean_sentiment.json: Contains the means of the sentiments over our whole corpus for each method of the following: "vader sentiment", "bert", "logistic regression 1", "logistic regression 2"
- word-graph directory:
  - .emb files: Node2Vec embeddings for the word graph
  - unclustered_*.gexf: Word graphs without clustered nodes
  - c_*.gexf: Word graphs with clustered nodes
