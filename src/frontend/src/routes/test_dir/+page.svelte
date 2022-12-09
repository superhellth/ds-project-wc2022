<script lang="ts">
    import Layout from "../../svelte-components/Layout.svelte";
    import ElasticHelper from "../../typescript/api_connections/elasticonnection";
    import Tweet from "../../typescript/tweet_management/tweet";
    import {Row, Spinner} from "sveltestrap";
    import TweetCard from "../../svelte-components/TweetCard.svelte";

    // Our connection to the middleware
    const elasticHelper: ElasticHelper = new ElasticHelper();

    // We get the stream rule, stream status and a list of the 50 most recent tweets asynchronously,
    // thus the data type is Promise
    const tweets: Promise<Array<Tweet>> = elasticHelper.getTweets();
</script>

<Layout>
    <div>
    {#await tweets}
        <div class="d-flex justify-content-center mt-4">
            <strong>Loading Tweets...</strong>
            <div class="spinner-border ml-4" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    {:then tweets}
      <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
        {#each tweets as aTweet}
            <div>
                <TweetCard data={aTweet}/>
            </div>
        {/each}
      </Row>
    {/await}
  </div>
</Layout>
