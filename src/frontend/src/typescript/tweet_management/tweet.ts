import TwitterUser from "./twitter-user";

/**
 * Our ts class for Tweets. Stores and provied all data we have about a tweet. (Not yet though -_-)
 */
class Tweet {

    private attachments: any;
    private author: TwitterUser;
    private created_at: Date;
    private geo: string;
    private id: string;
    private lang: string;
    private possibly_sensitive: boolean;
    private retweet_count: number;
    private reply_count: number;
    private like_count: number;
    private quote_count: number;
    private text: string;

    constructor(attachments: any, author: TwitterUser, created_at: Date, geo: string, id: string, lang: string, possibly_sensitive: boolean,
        retweet_count: number, reply_count: number, like_count: number, quote_count: number, text: string) {
        this.attachments = attachments;
        this.author = author;
        this.created_at = created_at;
        this.geo = geo;
        this.id = id;
        this.lang = lang;
        this.possibly_sensitive = possibly_sensitive;
        this.retweet_count = retweet_count;
        this.reply_count = reply_count;
        this.like_count = like_count;
        this.quote_count = quote_count;
        this.text = text;
    }

    /**
     * Parse Tweet from json format to ts object.
     * @param json json file to parse to tweet.
     * @returns the parsed tweet object.
     */
    public static fromJson(json: any): Tweet {
        json = json._source
        const attachments: any = json.attachments;
        const author: TwitterUser = TwitterUser.fromJson(json.author);
        const created_at: Date = new Date(json.created_at);
        const geo: string = json.geo;
        const id: string = json.id;
        const lang: string = json.string;
        const possibly_sensitive: boolean = json.possibly_sensitive;
        const retweet_count: number = json.public_metrics.retweet_count;
        const reply_count: number = json.public_metrics.reply_count;
        const like_count: number = json.public_metrics.like_count;
        const quote_count: number = json.public_metrics.quote_count;
        const text: string = json.text;
        return new Tweet(attachments, author, created_at, geo, id, lang, possibly_sensitive, retweet_count, reply_count, like_count, quote_count, text);
    }

    public getAgeInHours(): string {
        const today: Date = new Date();
        var one_minute: number = 1000 * 60;
        var now_millies: number = today.getTime();
        var created_at_millies: number = this.created_at.getTime();

        var difference_millies: number = now_millies - created_at_millies;
        var minutes_ago: number = Math.round(difference_millies / one_minute);
        var hours_ago: number = Math.round(minutes_ago / 60);
        var days_ago: number = Math.round(hours_ago / 24);

        var age_string: string = minutes_ago + " minutes";
        if (days_ago == 1) {
            age_string = "1 day"
        } else if (days_ago > 1) {
            age_string = days_ago + " days"
        } else if (hours_ago == 1) {
            age_string = "1 hour";
        } else if (hours_ago > 1) {
            age_string = hours_ago + " hours";
        }

        return age_string;
    }

    public getAttachments(): any {
        return this.attachments;
    }

    public getAuthor(): TwitterUser {
        return this.author;
    }

    public getCreatedAt(): Date {
        return this.created_at;
    }

    public getGeo(): string {
        return this.geo;
    }

    public getID(): string {
        return this.id;
    }

    public getLang(): string {
        return this.lang;
    }

    public isSensitive(): boolean {
        return this.possibly_sensitive;
    }

    public getRetweetCount(): number {
        return this.retweet_count;
    }

    public getReplyCount(): number {
        return this.reply_count;
    }

    public getLikeCount(): number {
        return this.like_count;
    }

    public getQuoteCount(): number {
        return this.quote_count;
    }

    public getText(): string {
        return this.text;
    }

}

export default Tweet;