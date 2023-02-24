# Data Files

### `generator-model`
- Features a fine-tuned GPT-neo model that was trained on a subset of random tweets from our dataset
- Data in `training_data.txt`

### `sentiment-data`
- `category_sent.json`: Sentiment values by all 4 methods for the 11 clusters we identified
- `classification.csv`: This file contains classifier training data. We created it ourselves by annotating ~1000 of our own Tweets with a multi-label system. Each Tweet (only represented by it's ID) has a sentiment (positive, neutral, negative) and one or more of the following labels: "match specific", "world cup specific", "football related", "joke/meme", "personal comment", "political comment", "prediction", "news", "announcement", "spam/scam", "unrelated", "unclassifiable"
  - The train/test split was done randomly
  - `classification_with_text_XXX.csv`: Contains the same information as the `classification.csv` file appended by the tweets text
- `mean_sentiment.json`: Contains the mean sentiment over all tweets in our dataset
- `sentiment_over_time.json`: Contains the sentiment values by all methods by days/weeks/months
- `Tweets.csv`: This file contains sentiment analysis training data. Source: https://www.kaggle.com/datasets/yasserh/twitter-tweets-sentiment-dataset
  - The train test split was done randomly
  - `Tweets_train.csv`: Our training split of the file
  - `Tweets_test.csv`: Our test split of the file

### `sentiment-models`
- Contains our own trained models 
  - using for '...Other...' the `Tweets.csv` or
  - using for '...Own...' the `classification.csv` data as basis


### `word-embeddings`
- Features the tsne plots that are generated as `.png` files
- Contains the Word2Vec model (`w2v_epochs=100.emb*` files)


### `word-graph`
  - `.emb` files: Node2Vec embeddings for the word graph
  - `unclustered_*.gexf`: Word graphs without clustered nodes
  - `c_*.gexf`: Word graphs with clustered nodes
