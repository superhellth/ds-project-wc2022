<script lang="ts">
    // Import Svelte components used in this script
    import Layout from "../../svelte-components/Layout.svelte";
    import {Row} from "sveltestrap";
    import TweetCard from "../../svelte-components/TweetCard.svelte";
    import type Tweet from "../../typescript/tweet_management/tweet";
    import ElasticProvider from "../../typescript/api_connections/elasticProvider";

    // Our connection to the middleware
    const elasticProvider: ElasticProvider = ElasticProvider.getInstance();

    // We get  a list of the 50 most recent tweets asynchronously, thus the data type is Promise
    // const tweets: Promise<Array<Tweet>> = elasticHelper.getTweets();
    const query = String.raw`{
        "sort": [{"created_at": "desc"}],
        "size": 50
    }`
    const tweets_100: Promise<Array<Tweet>> = elasticProvider.getTweetsThat(query);
</script>

<!-- Use the Layout component to define the overall layout of the page -->
<Layout>
    <div>
        <!-- TODO: Add rule/query management/overview like in the old layout (IF we want to use it) -->
    </div>
    <div>
        {#await tweets_100}
            <!-- Display a loading spinner while the tweets are being retrieved -->
            <div class="d-flex justify-content-center mt-4">
                <strong class="text-twitter-color">Loading Tweets...</strong>
                <div class="spinner-border ml-4 text-twitter-color">
                </div>
            </div>
        {:then tweets_100}
            <!-- Use the Row component from sveltestrap to create a responsive grid -->
            <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
                {#each tweets_100 as aTweet}
                    <!-- For each tweet, use the TweetCard component to display the tweet -->
                    <div>
                        <TweetCard data={aTweet}/>
                    </div>
                {/each}
            </Row>
        {/await}
    </div>
</Layout>
