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

    public async getTweetsByDayStats(): Promise<Map<Date, number>> {
        const data = await fetch(this.URL + "/statistics/tweetsPerDay").
        then((response) => response.json());

        const map: Map<Date, number> = new Map(Object.entries(data).map(([key, value]) => [new Date(key), Number(value)]));

        return map;
    }
}

export default ElasticProvider;