import Tweet from "../tweet_management/tweet";
import Connection from "./connection";

/**
 * This singeleton class manages all data retrieval tasks related to the middleware.
 */
class ElasticProvider extends Connection {
    private static instance: ElasticProvider;

    private constructor(URL: string) {
        super(URL);
    }

    public static getInstance(): ElasticProvider {
        if (!ElasticProvider.instance) {
            ElasticProvider.instance = new ElasticProvider("http://127.0.0.1:8000");
        }
        return ElasticProvider.instance;
    }

    /**
     * Query tweets from elasticsearch.
     * @param query The query to be forwarded to es.
     * @returns The queried tweets as an ArrayPromise.
     */
    public async getTweetsThat(query: string): Promise<Array<Tweet>> {
        // async request
        const data = await fetch(this.URL + "/query?query=" + query).
            then((response) => response.json());

        // convert to classes
        const tweetList = new Array<any>();
        for (let i = 0; i < data.length; i++) {
            tweetList.push(Tweet.fromJson(data[i]));
        }

        tweetList.sort(function (tweetA, tweetB) { return tweetB.getCreatedAt() - tweetA.getCreatedAt() });

        return tweetList;
    }

    /**
     * bla bla bla.
     * @returns Days mapped to the number of tweets collected that day.
     */
    public async getTweetsByDayStats(): Promise<Map<Date, number>> {
        const data = await fetch(this.URL + "/statistics/tweetsPerDay").
            then((response) => response.json());

        const map: Map<Date, number> = new Map(Object.entries(data).map(([key, value]) => [new Date(key), Number(value)]));

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

    public async getWordGraph(windowSize: number, numEdges: number, includeStopWords: boolean, minNodeLength: number, embeddingSize: number, clusterAlg: string, nClusters: number): Promise<string> {
        let includeStopWordsString: string = includeStopWords ? "True" : "False";
        let queryURL: string = this.URL + "/analysis/graph?window_size=" + windowSize + "&num_edges=" + numEdges + "&include_stop_words=" + includeStopWordsString
            + "&min_node_length=" + minNodeLength + "&embedding_size=" + embeddingSize + "&cluster_alg=" + clusterAlg + "&n_clusters=" + nClusters;
        const data = await fetch(queryURL).then((response) => response.text())
        return data
    }
}

export default ElasticProvider;