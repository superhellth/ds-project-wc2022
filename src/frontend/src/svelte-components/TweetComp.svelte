<script lang="ts">
    import Card, { Content } from "@smui/card";
    import Fab from "@smui/fab";
    import { Image } from "@smui/image-list";
    import type Tweet from "../typescript/tweet_management/tweet";

    export let tweet: Tweet;

</script>

<Card variant="outlined">
    <Content>
        <Fab style="max-width: 3em; max-height: 3em; float: left">
            <Image
                style="-webkit-border-radius: 10em; shape-radius: 5em "
                src={tweet.getAuthor().getProfileImageURL()} stand in image
            />
        </Fab>
        <h4>
            <span class="name" style="margin-left: 0.5em;">{tweet.getAuthor().getName()}</span>
            <span class="username">@{tweet.getAuthor().getUsername()}</span>
            <span class="username">- {tweet.getAgeInHours()}</span>
        </h4>
        <p class="tweet">{tweet.getText()}</p>
    </Content>
</Card>

<style>
    h4 {
        margin: 0em;
    }
    p {
        margin-top: 0.25em;
        margin-left: 3em;
    }
    span {
        vertical-align: middle;
    }
    span.username {
        color: #898989;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        font-style: normal;
        font-weight: lighter;
    }
    span.name {
        color: black;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        font-style: normal;
        font-weight: bold;
    }
    p.tweet {
        color: black;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        font-style: normal;
        font-weight: lighter;
    }
</style>
