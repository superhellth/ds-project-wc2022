import Tweet from "../tweet_management/tweet";
import Connection from "./connection";

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
            GenerateTweetProvider.instance = new GenerateTweetProvider("http://0.0.0.0:8003");
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
}

export default GenerateTweetProvider;