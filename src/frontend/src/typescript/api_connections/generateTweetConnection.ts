import Connection from "./connection";
import {
    PUBLIC_TWEET_GENERATION_MIDDLEWARE_PORT
} from '$env/static/public';

/**
 * This singeleton class manages all data retrieval tasks related to the middleware.
 */
class GenerateTweetProvider extends Connection {
    private static instance: GenerateTweetProvider;

    private constructor(URL: string) {
        super(URL);
    }

    public static getInstance(): GenerateTweetProvider {
        if (!GenerateTweetProvider.instance) {
            GenerateTweetProvider.instance = new GenerateTweetProvider("http://localhost:" + PUBLIC_TWEET_GENERATION_MIDDLEWARE_PORT);
        }
        return GenerateTweetProvider.instance;
    }

    public async getFineTunedTweets(prompt: string, temperature: string, repetition_penalty: string,
                                    length_penalty: string, n: string) {
        const queryURL = this.URL + '/analysis/finetunedgptneo/generate?prompt=' + prompt +
            "&temperature=" + temperature +
            "&repetition_penalty=" + repetition_penalty +
            "&length_penalty=" + length_penalty +
            "&n=" + n;
        const data = await fetch(queryURL).then((response) => response.json());
        return await data;
    }

    /**
     * Get completed Tweet. Completion based on n-grams.
     * @param given Start of the tweet text. This string will be completed.
     * @param tweetLength Number of tokens to append to given.
     * @param n n in n-gram.
     * @param topPercentage Number of n-grams to consider when completing the text. The higher this value more less frequent n-grams will be considered.
     * @param allowRepition Allow repition of n-grams in completion.
     * @returns The completed tweet as string.
     */
    public async getCompletedTweet(given: string, tweetLength: number, n: number, topPercentage: number, allowRepition: boolean): Promise<string> {
        let repitionString: string = allowRepition ? "True" : "False"
        let queryURL: string = this.URL + "/analysis/ngrams/generate?given=" + given + "&tweet_length=" + tweetLength + "&n=" + n
            + "&percent_n_grams=" + topPercentage + "&allow_repitition=" + repitionString;
        const data = await fetch(queryURL).then((response) => response.text());
        return data.replaceAll('"', '');
    }
}

export default GenerateTweetProvider;