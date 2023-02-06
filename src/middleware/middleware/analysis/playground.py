from middleware.analysis import tweet_provider

provider = tweet_provider.TweetProvider()
es_client = provider.get_client()
resp = es_client.search(index="tweets", body={
    "aggs": {
        "type_count": {
            "cardinality": {
                "field": "author.location"
            }
        }
    }
}, timeout="1m", request_timeout=120, size=0)

print(resp)
