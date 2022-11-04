def get_index_structure():
    index_structure = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 1
        },

        "mappings": {
            "properties": {
                "tweet_id": {"type": "unsigned_long", "index": "not_analyzed"},
                "author": {
                    "id": {"type": "unsigned_long", "index": "not_analyzed"},
                    "name": {"type": "string", "index": "not_analyzed"},
                    "username": {"type": "string", "index": "not_analyzed"},
                    "follower_count": {"type": "integer", "index": "not_analyzed"}
                },
                "created_at": {"type": "date", "index": "not_analyzed"},
                "like_count": {"type": "integer", "index": "not_analyzed"},
                "retweet_count": {"type": "integer", "index": "not_analyzed"},
                "reply_count": {"type": "integer", "index": "not_analyzed"},
                "text": {"type": "string", "index": "analyzed"}
            }
        }
    }
    return index_structure
 