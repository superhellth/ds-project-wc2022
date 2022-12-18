<script lang="ts">
    // Import Svelte components used in this script
    import Layout from "../../svelte-components/Layout.svelte";
    import { Button, Form, FormGroup, Input, Row } from "sveltestrap";
    import TweetCard from "../../svelte-components/TweetCard.svelte";
    import type Tweet from "../../typescript/tweet_management/tweet";
    import ElasticProvider from "../../typescript/api_connections/elasticProvider";
    import Label from "@smui/list/src/Label.svelte";
    import { onMount } from "svelte";

    // Our connection to the middleware
    const elasticProvider: ElasticProvider = ElasticProvider.getInstance();

    // We get  a list of the 50 most recent tweets asynchronously, thus the data type is Promise
    // const tweets: Promise<Array<Tweet>> = elasticHelper.getTweets();
    let query = String.raw`{
        "query": {
            "match": {
                "text": "Elasticsearch"
            }
        }
    }`;
    let isValid = true;

    $: {
        checkQueryValidity(query);
    }

    async function checkQueryValidity(query: string) {
        isValid = await elasticProvider.validateQuery(query);
    }

    let tweets_100: Promise<Array<Tweet>> =
        elasticProvider.getTweetsThat(query);

    let inner: HTMLTextAreaElement;
    const resize = () => {
        inner.style.height = "auto";
        inner.style.height = 4 + inner.scrollHeight + "px";
    };

    function executeQuery() {
        tweets_100 = elasticProvider.getTweetsThat(query);
    }

    onMount(async () => {
        resize();
    });
</script>

<!-- Use the Layout component to define the overall layout of the page -->
<Layout>
    <Form>
        <FormGroup>
            <Label>Tweet query</Label>
            <Input
                type="textarea"
                bind:inner
                bind:value={query}
                on:input={resize}
                feedback={isValid ? "Valid query" : "potentially invalid query"}
                valid={isValid}
                invalid={!isValid}
            />
            <Button type="button" on:click={executeQuery}>Execute Query</Button>
        </FormGroup>
    </Form>
    <div>
        {#await tweets_100}
            <!-- Display a loading spinner while the tweets are being retrieved -->
            <div class="d-flex justify-content-center mt-4">
                <strong class="text-twitter-color">Loading Tweets...</strong>
                <div class="spinner-border ml-4 text-twitter-color" />
            </div>
        {:then tweets_100}
            <!-- Use the Row component from sveltestrap to create a responsive grid -->
            <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
                {#each tweets_100 as aTweet}
                    <!-- For each tweet, use the TweetCard component to display the tweet -->
                    <div>
                        <TweetCard data={aTweet} />
                    </div>
                {/each}
            </Row>
        {/await}
    </div>
</Layout>
