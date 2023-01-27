from middleware.analysis.tweet_provider import TweetProvider

class BasicStatProvider:
    """Provides basic statistics about our tweet corpus.
    """

    def __init__(self) -> None:
        self.es_client = TweetProvider().get_client()

    def get_number_of_tweets(self, query={"match_all": {}}):
        """Count the number of documents matching the query.

        Args:
            query (dict, optional): Query. Defaults to {"match_all": {}}.

        Returns:
            int: Number of matches.
        """
        res = self.es_client.search(index="tweets", query=query, size=0, track_total_hits=True, timeout="1m")
        return res["hits"]["total"]["value"]
    
    def get_histogram(self, field, interval, histogram_type="histogram"):
        """Calculate histogram on a specified field.

        Args:
            field (str): field name to perform histogram on.
            interval (int): bucket size.
            histogram_size (str): type of the histogram, one of: date_histogram, histogram, terms

        Returns:
            dict: keys are buckets, values are doc counts.
        """
        if histogram_type == "terms":
            int_key = "size"
        else:
            int_key = "interval"
        resp = self.es_client.search(index="tweets", body={
            "size": 0,
            "aggs": {
                "hist": {
                    histogram_type: {
                        "field": field,
                        int_key: interval
                    }
                }
            }
        }, timeout="2m")

        # Access the dates and aggregated numbers from the response
        buckets = resp['aggregations']['hist']['buckets']
        if histogram_type == "date_histogram":
            key_str = "key_as_string"
        else:
            key_str = "key"
        bucket_dict = dict()
        for bucket in buckets:
            key = bucket[key_str]
            count = bucket['doc_count']
            bucket_dict[key] = count
        return bucket_dict
