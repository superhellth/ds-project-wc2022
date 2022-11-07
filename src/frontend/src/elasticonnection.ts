import Tweet from "./tweet_management/tweet";

class ElasticHelper {

  private static FASTAPI_URL: string = "http://45.13.59.173:8000";

  public async getTweets(): Promise<Array<Tweet>> {
    // async request
    let data = await fetch(ElasticHelper.FASTAPI_URL + "/query").then((response) => response.json());

    // convert to classes
    const tweetList = new Array<any>();
    for (var i = 0; i < data.length; i++) {
      tweetList.push(Tweet.fromJson(data[i]));
    }

    tweetList.sort(function(tweetA, tweetB) {return tweetB.getCreatedAt() - tweetA.getCreatedAt()});

    return tweetList;
  }

  public async setRule(rule: string): Promise<string> {
    const encodedRule = rule.replaceAll("#", "hashtag");
    const data = await fetch(ElasticHelper.FASTAPI_URL + "/stream/setRule/?rule=" + encodedRule).then((response) => response.json());

    return data.rule;
  }

  public async startStream(): Promise<boolean> {
    const data = await fetch(ElasticHelper.FASTAPI_URL + "/stream/start").then((response) => response.json());

    return data.running;
  }

  public async stopStream(): Promise<boolean> {
    const data = await fetch(ElasticHelper.FASTAPI_URL + "/stream/stop").then((response) => response.json());

    return data.running;
  }

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

  public async getRule(): Promise<string> {
    const data = await fetch(ElasticHelper.FASTAPI_URL + "/stream/status").then((response) => response.json());
    return data.rule;
  }

  public async isStreamRunning(): Promise<boolean> {
    const data = await fetch(ElasticHelper.FASTAPI_URL + "/stream/status").then((response) => response.json());
    return data.running;
  }
}

export default ElasticHelper;