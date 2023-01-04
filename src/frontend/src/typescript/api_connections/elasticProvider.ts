import Tweet from "../tweet_management/tweet";
import Connection from "./connection";

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

    public async getTopKUnigrams(k: number, includeStopWords: boolean, onlyMentions: boolean, onlyHashtags: boolean): Promise<JSON> {
        let includeStopWordsString: string = includeStopWords ? "True" : "False";
        let onlyMentionsString: string = onlyMentions ? "True" : "False";
        let onlyHashtagsString: string = onlyHashtags ? "True" : "False";
        const data = await fetch(this.URL + "/analysis/unigrams/top?k=" + k + "&include_stop_words=" + includeStopWordsString + "&only_mentions=" + onlyMentionsString + "&only_hashtags=" + onlyHashtagsString).then((response) => response.json());
        return data;
    }
}

export default ElasticProvider;