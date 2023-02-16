<script lang="ts">
    import type Tweet from "src/typescript/tweet_management/tweet";

    // Import the Tweet type and the Card component from the sveltestrap library
    import {
        Card,
        CardBody,
        CardFooter,
        CardHeader,
        CardImg,
        Col,
        Icon,
        Progress,
        Row,
    } from "sveltestrap";

    // Define a variable for storing the tweet data
    export let data: Tweet;
    export let showDetails: boolean;
    export let sentimentMethod: string;
    export let sentimentScore: any;
    export let sentimentMethodIndex: number;

    // Define a variable for storing the shadow effect
    let shadow = "";

    // Define a function for adding the shadow effect when the mouse is over the element
    function onOver() {
        shadow = "shadow";
    }

    // Define a function for removing the shadow effect when the mouse is no longer over the element
    function onLeave() {
        shadow = "";
    }
</script>

<div class="h-100">
    <Card color="dark" outline class="mt-4 mb-4">
        <!-- Add a class to the div, which will be used to apply the hover effect -->
        <!-- svelte-ignore a11y-mouse-events-have-key-events -->
        <div
            on:mouseover={() => {
                onOver();
            }}
            class="{shadow} bg-tweet hover-effect"
            on:mouseleave={() => {
                onLeave();
            }}
        >
            <CardHeader>
                <!-- Use a row and columns to lay out the elements in the header -->
                <Row>
                    <Col xs="2">
                        <!-- Wrap the image in a div to properly size it -->
                        <div>
                            <CardImg
                                src={data.getAuthor().getProfileImageURL()}
                            />
                        </div>
                    </Col>
                    <Col xs="10">
                        <!-- Use the name and username of the author to create a link to their twitter profile -->
                        <h5>
                            {data.getAuthor().getName()} (<a
                                href="https://www.twitter.com/{data
                                    .getAuthor()
                                    .getUsername()}"
                                >@{data.getAuthor().getUsername()}</a
                            >)
                        </h5>
                    </Col>
                </Row>
                {#if showDetails}
                    <Row>
                        <p>
                            {data.getAuthor().getFollowerCount()} Follower
                            <br />
                            {data.getAuthor().getTweetCount()} Tweets
                        </p>
                    </Row>
                {/if}
            </CardHeader>
            <!-- Use the text method to get the text of the tweet -->
            <CardBody>
                {data.getText()}
            </CardBody>
            <CardFooter>
                {#if sentimentMethod != "None"}
                {#await sentimentScore}
                    <p>Fetching sentiment score...</p>
                {:then sentScore} 
                    <Progress value={(sentScore[sentimentMethodIndex] + 1) / 2 * 100} style="color: red">{sentScore[sentimentMethodIndex]}</Progress>
                {/await}
                {/if}
                <!-- Use an icon to indicate that this is a tweet, and the ageInHours method to show how long ago it was posted -->
                <Icon name="twitter" />
                {data.getAgeInHours()} ago
                {#if showDetails}
                    <p><br />Score: {data.getScore()}</p>
                    <p>ID: {data.getID()}</p>
                {/if}
            </CardFooter>
        </div>
    </Card>
</div>
