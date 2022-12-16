import Tweet from "../tweet_management/tweet";

/**
 * This class provides an interface to the fast-api-middlware. All communication to the middleware should be handled by this class.
 */
class ElasticHelper {

  private static DATA_RETRIEVAL_URL: string = "http://127.0.0.1:8000";
  private static DATA_COLLECTION_URL: string = "http://45.13.59.173:8000";

    /**
   *
   * @returns a list of the queried tweets.
   */
  public async getTweetsThat(query: string): Promise<Array<Tweet>> {
    // async request
      const data = await fetch(ElasticHelper.DATA_RETRIEVAL_URL + "/query?query=" + query).
      then((response) => response.json());

    // convert to classes
    const tweetList = new Array<any>();
    for (let i = 0; i < data.length; i++) {
      tweetList.push(Tweet.fromJson(data[i]));
    }

    tweetList.sort(function(tweetA, tweetB) {return tweetB.getCreatedAt() - tweetA.getCreatedAt()});

    return tweetList;
  }

  /**
   * Updates the rule of the stream.
   * @param rule the new rule that was set.
   * @returns the new rule of the stream. Mainly for display purposes.
   */
  public async setRule(rule: string): Promise<string> {
    const encodedRule = rule.replaceAll("#", "hashtag");
    const data = await fetch(ElasticHelper.DATA_COLLECTION_URL + "/stream/setRule/?rule=" + encodedRule).then((response) => response.json());

    return data.rule;
  }

  /**
   * Start the stream.
   * @returns the new running state of the stream.
   */
  public async startStream(): Promise<boolean> {
    const data = await fetch(ElasticHelper.DATA_COLLECTION_URL + "/stream/start").then((response) => response.json());

    return data.running;
  }

  /**
   * Stops the stream.
   * @returns the new running state of the stream.
   */
  public async stopStream(): Promise<boolean> {
    const data = await fetch(ElasticHelper.DATA_COLLECTION_URL + "/stream/stop").then((response) => response.json());

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
    console.log("in toggle before: " + isRunning);
    if (isRunning) {
      result = this.stopStream();
    } else {
      result = this.startStream();
    }
    console.log("in toggle after: " + isRunning);

    return result;
  }

  /**
   * 
   * @returns the current rule of the stream.
   */
  public async getRule(): Promise<string> {
    const data = await fetch(ElasticHelper.DATA_COLLECTION_URL + "/stream/status").then((response) => response.json());
    return data.rule;
  }

  /**
   * 
   * @returns the current running state of the stream
   */
  public async isStreamRunning(): Promise<boolean> {
    const data = await fetch(ElasticHelper.DATA_COLLECTION_URL + "/stream/status").then((response) => response.json());
    return data.running;
  }
}

export default ElasticHelper;