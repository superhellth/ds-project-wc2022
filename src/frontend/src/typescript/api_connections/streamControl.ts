import Connection from "./connection";

/**
 * Singleton class that controls and provides data about the twitter-api stream.
 */
class StreamControl extends Connection {

    private static instance: StreamControl;

    private constructor(URL: string) {
        super(URL);
    }

    public static getInstance(): StreamControl {
        if (!StreamControl.instance) {
            StreamControl.instance = new StreamControl("http://localhost:8002");
        }
        return StreamControl.instance;
    }

    /**
     * Updates the rule of the stream.
     * @param rule the new rule that was set.
     * @returns the new rule of the stream. Mainly for display purposes.
     */
    public async setRule(rule: string): Promise<string> {
        const encodedRule = rule.replaceAll("#", "hashtag");
        const data = await fetch(this.URL + "/stream/setRule/?rule=" + encodedRule).then((response) => response.json());

        return data.rule;
    }

    /**
     * Start the stream.
     * @returns the new running state of the stream.
     */
    public async startStream(): Promise<boolean> {
        const data = await fetch(this.URL + "/stream/start").then((response) => response.json());

        return data.running;
    }

    /**
     * Stops the stream.
     * @returns the new running state of the stream.
     */
    public async stopStream(): Promise<boolean> {
        const data = await fetch(this.URL + "/stream/stop").then((response) => response.json());

        return data.running;
    }

    /**
     * Toggles the stream:
     * turns it off, if its on,
     * turn it on, if its off.
     * @returns the new running state of the stream.
     */
    public async toggleStream(): Promise<boolean> {
        let result: Promise<boolean>;
        const isRunning = await this.isStreamRunning();
        if (isRunning) {
            result = this.stopStream();
        } else {
            result = this.startStream();
        }

        return result;
    }

    /**
     *
     * @returns the current rule of the stream.
     */
    public async getRule(): Promise<string> {
        try {
            const data = await fetch(this.URL + "/stream/status").then((response) => response.json());
            return data.rule;
        } catch (error) {
            return "Not Found. The data collection middleware component is probably not running"
        }
    }

    /**
     *
     * @returns the current running state of the stream
     */
    public async isStreamRunning(): Promise<boolean> {
        try {
            const data = await fetch(this.URL + "/stream/status").then((response) => response.json());
            return data.running;
        } catch (error) {
            return false
        }
    }
}

export default StreamControl;