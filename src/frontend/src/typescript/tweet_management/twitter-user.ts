/**
 * Our ts class for Twitter User. Stores and provied all data we have about a twitter user.
 */
class TwitterUser {

    private created_at: Date;
    private description: string;
    private id: string;
    private location: string;
    private name: string;
    private profile_image_url: string;
    private follower_count: number;
    private following_count: number;
    private tweet_count: number;
    private listed_count: number;
    private url: string;
    private username: string;
    private verified: boolean;

    public constructor(created_at: Date, description: string, id: string, location: string, name: string, profile_image_url: string,
        follower_count: number, following_count: number, tweet_count: number, listed_count: number, url: string, username: string, verified: boolean) {
        this.created_at = created_at;
        this.description = description;
        this.id = id;
        this.location = location;
        this.name = name;
        this.profile_image_url = profile_image_url;
        this.follower_count = follower_count;
        this.following_count = following_count;
        this.tweet_count = tweet_count;
        this.listed_count = listed_count;
        this.url = url;
        this.username = username;
        this.verified = verified;
    }

    public static fromJson(json: any): TwitterUser {
        const created_at: Date = json.created_at;
        const description: string = json.description;
        const id: string = json.id;
        const location: string = json.location;
        const name: string = json.name;
        const profile_image_url: string = json.profile_image_url;
        const follower_count: number = json.public_metrics.followers_count;
        const following_count: number = json.public_metrics.following_count;
        const tweet_count: number = json.public_metrics.tweet_count;
        const listed_count: number = json.public_metrics.listed_count;
        const url: string = json.url;
        const username: string = json.username;
        const verified: boolean = json.verified;
        return new TwitterUser(created_at, description, id, location, name, profile_image_url,
            follower_count, following_count, tweet_count, listed_count, url, username, verified);
    }

    public getName(): string {
        return this.name;
    }

    public getUsername(): string {
        return this.username;
    }

    public isVerified(): boolean {
        return this.verified;
    }

    public getProfileImageURL(): string {
        return this.profile_image_url;
    }

    public getFollowerCount(): number {
        return this.follower_count;
    }

}

export default TwitterUser;