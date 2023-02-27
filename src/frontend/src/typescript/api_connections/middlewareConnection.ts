import Tweet from "../tweet_management/tweet";
import Connection from "./connection";
import {
    PUBLIC_DATA_RETRIEVAL_MIDDLEWARE_PORT
} from '$env/static/public';

/**
 * This singeleton class manages all data retrieval tasks related to the middleware.
 */
class MiddlewareProvider extends Connection {
    private static instance: MiddlewareProvider;

    private constructor(URL: string) {
        super(URL);
    }

    public static getInstance(): MiddlewareProvider {
        if (!MiddlewareProvider.instance) {
            MiddlewareProvider.instance = new MiddlewareProvider("http://localhost:" + PUBLIC_DATA_RETRIEVAL_MIDDLEWARE_PORT);
        }
        return MiddlewareProvider.instance;
    }

    /**
     * Send a query directly to ES.
     * @param query Query to be passed to ES.
     * @returns Response as json.
     */
    public async queryESRaw(query: string): Promise<any> {
        // async request
        let data = await fetch(this.URL + "/query/raw?query=" + query).then((response) => response.json());
        return data;
    }

    /**
     * Query tweets from elasticsearch.
     * @param query The query to be forwarded to es.
     * @returns The queried tweets as an ArrayPromise.
     */
    public async getTweetsThat(query: string): Promise<Array<Tweet>> {
        // async request
        let data = await fetch(this.URL + "/query?query=" + query).then((response) => response.json());

        // convert to classes
        data = data.hits;
        const tweetList = new Array<any>();
        for (let i = 0; i < data.length; i++) {
            tweetList.push(Tweet.fromJson(data[i]));
        }

        tweetList.sort(function (tweetA, tweetB) {
            return tweetB.getCreatedAt() - tweetA.getCreatedAt()
        });

        return tweetList;
    }

    /**
     * Fetch a Tweet by ID from ES.
     * @param id ID of the Tweet to fetch.
     * @returns The Tweet with the given ID.
     */
    public async getTweetByID(id: bigint): Promise<Tweet> {
        let query = `{"query": {
            \t"term": {
            \t\t"id": ` + id + `
            \t}
            }}`;
        let data = await fetch(this.URL + "/query?query=" + query).then((response) => response.json());
        data = data.hits;
        return Tweet.fromJson(data[0])
    }

    /**
     * Count number of matching tweets in es index.
     * @param query The query to be forwarded to es.
     * @returns The number of matching tweets.
     */
    public async getNumberOfTweets(query: string): Promise<number> {
        // async request
        let data = await fetch(this.URL + "/query?query=" + query).then((response) => response.json());

        return data.counts;
    }

    /**
     * Get date histogram of specific field.
     * @param field Field to generate histogram on.
     * @param interval Time interval for buckets. One of day, month, year.
     * @returns Map from date to tweet count.
     */
    public async getDateHistogram(field: string, interval: string): Promise<Map<Date, number>> {
        const data = await fetch(this.URL + "/statistics/histogram?histogram_type=date_histogram&interval=" + interval + "&field=" + field).then((response) => response.json());

        const map: Map<Date, number> = new Map(Object.entries(data).map(([key, value]) => [new Date(key), Number(value)]));

        return map;
    }

    /**
     * Create term histogram on ES index.
     * @param field Field to create histogram on. Has to be a keyword field.
     * @param size Number of buckets (?).
     * @returns Histogram as Map<string, number>.
     */
    public async getTermHistogram(field: string, size: number): Promise<Map<string, number>> {
        const data = await fetch(this.URL + "/statistics/histogram?histogram_type=terms&interval=" + size + "&field=" + field).then((response) => response.json());

        const map: Map<string, number> = new Map(Object.entries(data).map(([key, value]) => [String(key), Number(value)]));

        return map;
    }

    /**
     * Does not work properly since all queries including a sort or size parameter are labelled as invalid.
     * @param query Query string to verify.
     * @returns Whether or not the query is valid.
     */
    public async validateQuery(query: string): Promise<boolean> {
        const data = await fetch(this.URL + "/validate?query=" + query).then((response) => response.json());
        return data.valid;
    }

    /**
     * Retrieve filtered tokens from the unigrams.json file.
     * @param k Number of top unigrams to return.
     * @param includeStopWords Include or filter out stop words.
     * @param onlyMentions Return only tokens that are mentions(start with '@')
     * @param onlyHashtags Return only tokens that are hashtags(start with '#)
     * @returns The k most common tokens that match the requirements.
     */
    public async getTopKUnigrams(k: number, includeStopWords: boolean, onlyMentions: boolean, onlyHashtags: boolean): Promise<Object> {
        let includeStopWordsString: string = includeStopWords ? "True" : "False";
        let onlyMentionsString: string = onlyMentions ? "True" : "False";
        let onlyHashtagsString: string = onlyHashtags ? "True" : "False";
        const data = await fetch(this.URL + "/analysis/unigrams/top?k=" + k + "&include_stop_words=" + includeStopWordsString + "&only_mentions=" + onlyMentionsString
            + "&only_hashtags=" + onlyHashtagsString).then((response) => response.json());
        return data;
    }

    /**
     * Retrieve the most common n-grams.
     * @param n n in n-gram.
     * @param k Number of top unigrams to return.
     * @returns The k most common n-grams as Object. Map-like: string as key, number as value.
     */
    public async getTopKNGrams(n: number, k: number): Promise<Object> {
        const data = await fetch(this.URL + "/analysis/ngrams/top?n=" + n + "&k=" + k).then((response) => response.json());
        return data;
    }

    /**
     * Query the middleware to get a graph with specific parameters. If the graph does not exist yet, it will be generated.
     * @param windowSize Window size for the collocations to use.
     * @param numEdges The number of collocations (ordered by count) used to generate graph.
     * @param includeStopWords Include nodes that are stop words.
     * @param minNodeLength Minimum number of characters in node name.
     * @param embeddingSize Size of the Node2Vec embedding.
     * @param clusterAlg Algorithm used to cluster the graph.
     * @param nClusters Number of clusters to generate.
     * @returns The graph file as string.
     */
    public async getWordGraph(windowSize: number, numEdges: number, includeStopWords: boolean, minNodeLength: number, embeddingSize: number, clusterAlg: string, nClusters: number, nesOnly: boolean): Promise<string> {
        let includeStopWordsString: string = includeStopWords ? "True" : "False";
        if (nesOnly) {
            windowSize = 0;
        }
        let nesOnlyString: string = nesOnly ? "True" : "False";
        let queryURL: string = this.URL + "/analysis/graph?window_size=" + windowSize + "&num_edges=" + numEdges + "&include_stop_words=" + includeStopWordsString
            + "&min_node_length=" + minNodeLength + "&embedding_size=" + embeddingSize + "&cluster_alg=" + clusterAlg + "&n_clusters=" + nClusters + "&only_nes=" + nesOnlyString;
        const data = await fetch(queryURL).then((response) => response.text());
        return data;
    }

    /**
     * Check if word has embedding.
     * @param word Word to check if embedding exists for.
     * @returns Whether or not word has embedding.
     */
    public async existsInW2vecVocabulary(word: string): Promise<boolean> {
        let queryURL: string = this.URL + "/analysis/embedding/exists?word=" + word;
        const data = await fetch(queryURL).then((response) => response.text());
        return data == "true";
    }

    /**
     * Find unfitting word in list based on Word2Vec embedding.
     * @param words List of words to check.
     * @returns The word in the list that does not fit in.
     */
    public async doesntMatch(words: string[]): Promise<string> {
        let argString: string = "";
        for (let i = 0; i < words.length; i++) {
            argString += "word=" + words[i] + "&";
        }
        let queryURL: string = this.URL + "/analysis/embedding/doesntmatch?" + argString.substring(0, argString.length - 1);
        const data = await fetch(queryURL).then((response) => response.text());
        return data;
    }

    /**
     * Get similar words based on Word2Vec embedding.
     * @param positive Positive contributions.
     * @param negative Negative contributions.
     * @returns Top 10 most similar words.
     */
    public async getSimilar(positive: string[], negative: string[]): Promise<Map<string, number>> {
        let argString: string = "&";
        for (let i = 0; i < positive.length; i++) {
            argString += "positive=" + positive[i] + "&"
        }
        for (let i = 0; i < negative.length; i++) {
            argString += "negative=" + negative[i] + "&"
        }
        let queryURL: string = this.URL + "/analysis/embedding/similar?" + argString.substring(0, argString.length - 1);
        const data = await fetch(queryURL).then((response) => response.json());

        return data.similar;
    }

    /**
     * Get distance between 2 words based on Word2Vec embedding.
     * @param word1 Word 1.
     * @param word2 Word 2.
     * @returns Distance between Word 1 and Word 2.
     */
    public async getDistance(word1: string, word2: string): Promise<number> {
        let queryURL = this.URL + "/analysis/embedding/distance?word1=" + word1 + "&word2=" + word2;
        const data = await fetch(queryURL).then((response) => response.text());
        return Number.parseFloat(data);
    }

    /**
     * Get link to generated TSNE plot with given parameters.
     * @param word Word to build plot around.
     * @param numCloseWords Number of close words to display on plot.
     * @param numFarWords Number of far away words to display on plot.
     * @returns Link to generated plot.
     */
    public getTSNEPlotURL(word: string, numCloseWords: number, numFarWords: number, filePrefix: string): string {
        let queryURL: string = this.URL + "/analysis/embedding/tsne?word=" + word + "&num_closest=" + numCloseWords + "&num_furthest=" + numFarWords + "&file_prefix=" + filePrefix;
        return queryURL;
    }

    public async getAvgSentimentTweetsList(tweetsList: Array<string>) {
        const queryURL = this.URL + '/analysis/sentiment/tweetsListAvg';
        const response = await fetch(queryURL, {
            method: "POST",
            body: JSON.stringify(tweetsList),
            headers: { "Content-Type": "application/json" },
        });
        return await response.json();
    }

    public async getSentimentTweet(tweet: string) {
        const queryURL = this.URL + '/analysis/sentiment/tweet';
        const response = await fetch(queryURL, {
            method: "POST",
            body: JSON.stringify({ tweet_text: tweet }),
            headers: { "Content-Type": "application/json" },
        });
        return await response.json();
    }

    public async getMeanOverallSentiment() {
        let queryURL: string = this.URL + "/analysis/sentiment/meanSentiment";
        return await fetch(queryURL).then((response) => response.json());
    }

    public async getTrainedModelPerformance() {
        let queryURL: string = this.URL + "/analysis/sentiment/trainedModelPerformance";
        return await fetch(queryURL).then((response) => response.json());
    }

    public async getSentimentOverTime() {
        let queryURL: string = this.URL + "/analysis/sentiment/sentimentOverTime";
        return await fetch(queryURL).then((response) => response.json());
    }

    public async getSentimentByCategory() {
        let queryURL: string = this.URL + "/analysis/sentiment/sentimentByCategory";
        return await fetch(queryURL).then((response) => response.json());
    }

    public async getQatarSentiment() {
        let queryURL: string = this.URL + "/analysis/sentiment/qatarSentiment";
        return await fetch(queryURL).then((response) => response.json());
    }
}

export default MiddlewareProvider;