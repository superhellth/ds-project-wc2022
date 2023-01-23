<script lang="ts">
    // Import Svelte components used in this script
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
    let query = `"query": {
\t"match": {
\t\t"text": "Infantino"
\t}
}`;
    let isValid = true;
    let sizeOptions = [10, 20, 50, 100];
    let currentSize = sizeOptions[0];
    let sortOptions = [
        "_score",
        "created_at",
        "possibly_sensitive",
        "public_metrics.retweet_count",
        "public_metrics.reply_count",
        "public_metrics.like_count",
        "public_metrics.quote_count",
        "author.created_at",
        "author.name",
        "author.username",
        "author.verified",
        "author.public_metrics.followers_count",
        "author.public_metrics.following_count",
        "author.public_metrics.tweet_count",
        "author.public_metrics.listed_count",
    ];
    let currentSort = sortOptions[0];
    let sortAscending = false;
    let showDetails = false;

    $: {
        checkQueryValidity(query);
    }

    async function checkQueryValidity(query: string) {
        isValid = await elasticProvider.validateQuery("{" + query + "}");
    }

    let tweets_100: Promise<Array<Tweet>> = elasticProvider.getTweetsThat(
        getFullQuery()
    );

    let inner: HTMLTextAreaElement;
    const resize = () => {
        inner.style.height = "auto";
        inner.style.height = 4 + inner.scrollHeight + "px";
    };

    function getFullQuery(): string {
        let sortString = sortAscending ? `"asc"` : `"desc"`;
        let fullQuery =
            "{\n" +
            query +
            `,
    "size" : ` +
            currentSize +
            `,
    "sort" : {` +
            `"` +
            currentSort +
            `":` +
            sortString +
            `}` +
            "\n}";
        return fullQuery;
    }

    function executeQuery() {
        tweets_100 = elasticProvider.getTweetsThat(getFullQuery());
    }

    onMount(async () => {
        resize();
        let queryInput = document.getElementById("query-input")!;
        queryInput.style.backgroundColor = "#212529";
        queryInput.style.color = "#FFFFFF";
        queryInput.addEventListener("keydown", function (e) {
            if (e.key == "Tab") {
                e.preventDefault();
                var start = this.selectionStart;
                var end = this.selectionEnd;

                // set textarea value to: text before caret + tab + text after caret
                this.value =
                    this.value.substring(0, start) +
                    "\t" +
                    this.value.substring(end);

                // put caret at right position again
                this.selectionStart = this.selectionEnd = start + 1;
            }
        });
    });
</script>

<title>Overwiev - Tweets</title>
<Form>
    <h2>Tweet query</h2>
    <FormGroup>
        <Input
            id="query-input"
            type="textarea"
            bind:inner
            bind:value={query}
            on:input={resize}
            feedback={isValid ? "Valid query" : "potentially invalid query"}
            valid={isValid}
            invalid={!isValid}
        />
    </FormGroup>
    <div style="display: flex; justify-content: space-between">
        <FormGroup>
            <Label for="exampleSelect">Sort by</Label>
            <Input
                type="select"
                name="select"
                id="exampleSelect"
                style="width: 25em"
                bind:value={currentSort}
            >
                {#each sortOptions as option}
                    <option>{option}</option>
                {/each}
            </Input>
            <Input
                type="checkbox"
                label="Ascending"
                checked={sortAscending}
                on:input={() => (sortAscending = !sortAscending)}
            />
        </FormGroup>
        <FormGroup>
            <Label for="exampleSelect">Count</Label>
            <Input
                type="select"
                name="select"
                id="exampleSelect"
                style="width: 5em"
                bind:value={currentSize}
            >
                {#each sizeOptions as option}
                    <option>{option}</option>
                {/each}
            </Input>
        </FormGroup>
        <FormGroup>
            <Button type="button" on:click={executeQuery}>Execute Query</Button>
            <Input
                type="checkbox"
                label="Show Details"
                checked={showDetails}
                on:input={() => (showDetails = !showDetails)}
            />
        </FormGroup>
    </div>
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
                    <TweetCard data={aTweet} bind:showDetails />
                </div>
            {/each}
        </Row>
    {/await}
</div>
