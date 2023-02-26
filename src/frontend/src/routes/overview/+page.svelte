<script lang="ts">
    // Import Svelte components used in this script
    import {
        Button,
        Form,
        FormGroup,
        Input,
        Row,
        Table,
        Accordion,
        AccordionItem,
        Popover,
        Breadcrumb,
        BreadcrumbItem,
    } from "sveltestrap";
    import TweetCard from "src/svelte-components/TweetCard.svelte";
    import type Tweet from "src/typescript/tweet_management/tweet";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import Label from "@smui/list/src/Label.svelte";
    import {onMount} from "svelte";
    import {fly} from "svelte/transition";

    // Our connection to the middleware
    const elasticProvider: MiddlewareProvider =
        MiddlewareProvider.getInstance();

    // Declaring variables to store the query, the validity of the query, options for size, sorting, and sentiment analysis.
    let query = `"query": {
\t"match_phrase": {
\t\t"text": "Human rights"
\t}
}`;
    let isValid: boolean = true;
    let sizeOptions: Array<number> = [10, 20, 50, 100];
    let currentSize: number = sizeOptions[0];
    let sortOptions: string[] = [
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
    let currentSort: string = sortOptions[0];
    let sortAscending: boolean = false;
    let showDetails: boolean = false;
    let showSentimentForMethod: Map<string, number> = new Map<string, number>();
    showSentimentForMethod.set("None", -1);
    showSentimentForMethod.set("VaderSentiment", 0);
    showSentimentForMethod.set("SGDClassifierOther", 1);
    showSentimentForMethod.set("SGDClassifierOwn", 2);
    showSentimentForMethod.set("BERT", 3);
    let selectedSentimentMethod: string = "None";

    $: {
        checkQueryValidity(query);
    }

    async function checkQueryValidity(query: string) {
        try {
            isValid = await elasticProvider.validateQuery("{" + query + "}");
        } catch (error) {
            console.log("Failed to fetch")
        }
    }

    let tweetPromise: Promise<Array<Tweet>> = elasticProvider.getTweetsThat(
        getFullQuery()
    );
    let numberOfMatchingTweets: Promise<number> = elasticProvider.getNumberOfTweets(
        getFullQuery()
    );

    let inner: HTMLTextAreaElement;

    function resize() {
        inner.style.height = "auto";
        inner.style.height = 4 + inner.scrollHeight + "px";
    }

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

    async function executeQuery() {
        tweetPromise = elasticProvider.getTweetsThat(getFullQuery());
        numberOfMatchingTweets = elasticProvider.getNumberOfTweets(
            getFullQuery()
        );
        loaded_tweets = await tweetPromise;
        await analyzeSentiment();
    }

    // Sentiment stuff
    let loaded_tweets: Array<Tweet>; // variable to hold the tweets
    let vaderSent: string = "Waiting..."; // variable to hold the vaderSent score
    let trainedSent: string = "Waiting..."; // variable to hold the trainedSent score
    let nbSent: string = "Waiting..."; // variable to hold the nbSent score
    let bertSent: string = "Waiting... (BERT: I'm a bit slow, sorry!)"; // variable to hold the bertSent score

    // function to send tweets text to the sentiment analysis endpoint
    async function analyzeSentiment() {
        // Extract the text of each tweet
        let tweets_text = loaded_tweets.map((t) => t.getText());
        // Send the tweets text to the sentiment analysis endpoint
        vaderSent = "Waiting...";
        trainedSent = "Waiting...";
        nbSent = "Waiting...";
        bertSent = "Waiting... (BERT: I'm a bit slow, sorry!)";
        const scores = await elasticProvider.getAvgSentimentTweetsList(
            tweets_text
        );
        vaderSent = scores[0];
        trainedSent = scores[1];
        nbSent = scores[2];
        bertSent = scores[3];
    }

    let visible: boolean = false;

    onMount(async () => {
        resize();
        visible = true;
        let queryInput = document.getElementById("query-input")!;
        queryInput.style.backgroundColor = "var(--side-bar-color)";
        queryInput.style.color = "#FFFFFF";
        queryInput.addEventListener("keydown", function (e) {
            if (e.key == "Tab") {
                // Prevent the default behavior of the "Tab" key
                e.preventDefault();
                // Get the start and end positions of the text selection
                var start = this.selectionStart;
                var end = this.selectionEnd;

                // Insert a tab character into the textarea at the current caret position
                this.value =
                    this.value.substring(0, start) +
                    "\t" +
                    this.value.substring(end);

                // Reset the caret position to be immediately after the inserted tab character
                this.selectionStart = this.selectionEnd = start + 1;
            }
        });
        // Wait for the `executeQuery` function to complete before continuing
        await executeQuery();
    });
</script>

<title>Overview - Tweets</title>
<h1>Tweet Query</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Twitter Feed</BreadcrumbItem>
</Breadcrumb>

<Form>
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
                    style="width: 25em;"
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
            <Label for="exampleSelect">Displayed Results</Label>
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
{#await numberOfMatchingTweets}
    <p>Loading...</p>
{:then numTweets}
    <p># Tweets matching query: {numTweets}</p>
{/await}
{#key visible}
    <div in:fly={{ y: 200, duration: 500, delay: 400 }}>
        <Accordion>
            <AccordionItem>
                <h5 class="m-0" slot="header">Sentiment Analysis</h5>
                <div style="display: flex; justify-content: center">
                    <Form inline>
                        <FormGroup>
                            <Label
                            >Show sentiment for each Tweet by Method</Label
                            >
                            <Input
                                    type="select"
                                    name="select"
                                    id="exampleSelect"
                                    style="width: 20em"
                                    bind:value={selectedSentimentMethod}
                            >
                                {#each Array.from(showSentimentForMethod.keys()) as sentimentMethod}
                                    <option>{sentimentMethod}</option>
                                {/each}
                            </Input>
                        </FormGroup>
                    </Form>
                </div>
                <Table hover bordered>
                    <thead>
                    <tr>
                        <th>#</th>
                        <th>Method (More info on click)</th>
                        <th
                        >Sentiment Score (-1 to 1, 'negative' to
                            'positive')
                        </th
                        >
                    </tr>
                    </thead>
                    <tbody>
                    <tr>
                        <th scope="row">1</th>
                        <td id="vaderSentId">
                            <a href="">vaderSentiment</a>
                            <Popover placement="right" target="vaderSentId">
                                <div slot="title">
                                    <b>vaderSentiment</b>
                                </div>
                                This sentiment score is calculated by the<a
                                    href="https://github.com/cjhutto/vaderSentiment"
                            >
                                vaderSentiment
                            </a> SentimentIntensityAnalyzer class. It uses
                                a 'lexicon' and 'rule-based' approach and is
                                fine-tuned for social media sentiment analysis.
                            </Popover>
                        </td>
                        <td>{vaderSent}</td>
                    </tr>
                    <tr>
                        <th scope="row">2</th>
                        <td id="tcsgdSent">
                            <a href="">SGDClassifierOther</a>
                            <Popover placement="right" target="tcsgdSent">
                                <div slot="title">
                                    <b>SGDClassifier</b>
                                </div>
                                This sentiment score is calculated by the<a
                                    href="https://scikit-learn.org/stable/index.html"
                            >
                                sklearn
                            </a> SGDClassifier class in combination with
                                a TfidfVectorizer. It trains using a file with
                                26000 labeled tweets which can be found in our
                                repository under 'src/data/Tweets_train.csv'.
                            </Popover>
                        </td>
                        <td>{trainedSent}</td>
                    </tr>
                    <tr>
                        <th scope="row">3</th>
                        <td id="nbSent">
                            <a href="">SGDClassifierOwn</a>
                            <Popover placement="right" target="nbSent">
                                <div slot="title">
                                    <b>SGDClassifierOwn</b>
                                </div>
                                This sentiment score is calculated by the<a
                                    href="https://scikit-learn.org/stable/index.html"
                            >
                                sklearn
                            </a> SGDClassifier class in combination with
                                a TfidfVectorizer. It trains using a own self
                                labeled tweets from our dataset which can be
                                found in our repository under 'src/data/classification_with_text_train.csv'.
                            </Popover>
                        </td>
                        <td>{nbSent}</td>
                    </tr>
                    <tr>
                        <th scope="row">4</th>
                        <td id="bertSent">
                            <a href="">BERT based Classifier</a>
                            <Popover placement="right" target="bertSent">
                                <div slot="title">
                                    <b>BERT based Classifier</b>
                                </div>
                                This sentiment score is calculated by the<a
                                    href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english"
                            >
                                distilbert-base-uncased-finetuned-sst-2-english
                            </a> model as found on HuggingFace. In order
                                for the tweets to be processed 'properly' we
                                looked at the training data for that model. To
                                keep our input similar we decided to drop all
                                non-ascii symbols. We did not fine-tune the model.
                            </Popover>
                        </td>
                        <td>{bertSent}</td>
                    </tr>
                    </tbody>
                </Table>
            </AccordionItem>
        </Accordion>
    </div>
{/key}
<div>
    {#await tweetPromise}
        <!-- Display a loading spinner while the tweets are being retrieved -->
        <div class="d-flex justify-content-center mt-4">
            <strong class="text-twitter-color">Loading Tweets...</strong>
            <div class="spinner-border ml-4 text-twitter-color"/>
        </div>
    {:then tweets_100}
        <!-- Use the Row component from sveltestrap to create a responsive grid -->
        <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
            {#each tweets_100 as aTweet, i}
                <!-- For each tweet, use the TweetCard component to display the tweet -->
                <div in:fly={{ y: 200, duration: 500, delay: 200 * i }}>
                    <TweetCard
                            data={aTweet}
                            bind:showDetails
                            sentimentMethod={selectedSentimentMethod}
                            sentimentScore={elasticProvider.getSentimentTweet(
                            aTweet.getText()
                        )}
                            sentimentMethodIndex={showSentimentForMethod.get(
                            selectedSentimentMethod
                        )}
                    />
                </div>
            {/each}
        </Row>
    {/await}
</div>
