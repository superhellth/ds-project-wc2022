from pydoc import doc
from elasticsearch import helpers, Elasticsearch
from middleware.tweet_management import twitter_tweet

es_client = Elasticsearch("http://45.13.59.173:9200", http_auth=("elastic", "sicheristsicher"))
tweets = list()
for document in helpers.scan(es_client, index="tweets"):
    tweets.append(twitter_tweet.Tweet(document, is_es_doc=True))
    if len(tweets) % 1000 == 0:
        print(len(tweets))  
        
# resp = es_client.search(index="tweets", query={"match_all": {}})
# documents = resp["hits"]["hits"]
# for document in documents: