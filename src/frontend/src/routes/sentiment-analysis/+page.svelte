<script lang="ts">
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {Alert, Breadcrumb, BreadcrumbItem, Button, Col, Form, FormGroup, Input, Row} from "sveltestrap";
    import {onMount} from "svelte";
    import SentimentByCard from "../../svelte-components/SentimentByCard.svelte";
    import {fly} from "svelte/transition";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();

    // Overall Sentiment variables
    let userTweet: string = '';
    let vaderSentMean = 'Loading...';
    let lrcSentOtherMean = 'Loading...';
    let lrcSentOwnMean = 'Loading ...';
    let bertSentMean = 'Loading ...';

    // Try it out variables
    let vaderSent = 'Waiting...';
    let sgdSentOther = 'Waiting...';
    let sgdSentOwn = 'Waiting...';
    let bertSent = "Waiting... (BERT: I\'m a bit slow, sorry!)";

    // Trained model performance variables
    let otherAccuracyPercentage = 'Waiting...';
    let otherRecallPercentage = 'Waiting...';
    let otherF1Percentage = 'Waiting...';
    let ownF1Percentage = 'Waiting...';
    let ownAccuracyPercentage = 'Waiting...';
    let ownRecallPercentage = 'Waiting...';

    // Sent by topic variables
    const topics_mean = Array(11).fill('Waiting...');
    const topics_vs_sent = Array(11).fill('Waiting...');
    const topics_bert_sent = Array(11).fill('Waiting...');
    const topics_lrc_other = Array(11).fill('Waiting...');
    const topics_lrc_own = Array(11).fill('Waiting...');
    const topics_count = Array(11).fill('Waiting...');
    const titles = [
        'The Center Cluster', '#Cluster', '#SayTheirNames',
        'C\'mon England!', '???', 'Steve Harvey',
        'SUIIII!!!', 'NFT and Crypto', '你好中国人！',
        'Cluster 10', 'Stand with Ukraine'
    ];
    let showTopicSentDetails: boolean = false;

    // Add transition variables
    let transDuration: number = 600;


    // Function to get the sentiment by topic
    async function getSentimentByTopic() {
        const data = await provider.getSentimentByCategory();
        for (let i = 0; i < topics_mean.length; i++) {
            topics_mean[i] = sliceString(data[(i + 1).toString()]['mean_sent'].toString());
            topics_vs_sent[i] = sliceString(data[(i + 1).toString()]['vs_sent'].toString());
            topics_bert_sent[i] = sliceString(data[(i + 1).toString()]['bert_sent'].toString());
            topics_lrc_other[i] = sliceString(data[(i + 1).toString()]['lrc_other'].toString());
            topics_lrc_own[i] = sliceString(data[(i + 1).toString()]['lrc_own'].toString());
            topics_count[i] = sliceString(data[(i + 1).toString()]['count'].toString());
        }
    }

    // Function to get the trained model performance
    async function getTrainedModelPerf() {
        const [
            otherAccuracy,
            otherRecall,
            otherF1,
            ownF1,
            ownAccuracy,
            ownRecall
        ] = await provider.getTrainedModelPerformance();

        otherAccuracyPercentage = (otherAccuracy * 100).toFixed(2) + '%';
        otherRecallPercentage = (otherRecall * 100).toFixed(2) + '%';
        otherF1Percentage = (otherF1 * 100).toFixed(2) + '%';
        ownF1Percentage = (ownF1 * 100).toFixed(2) + '%';
        ownAccuracyPercentage = (ownAccuracy * 100).toFixed(2) + '%';
        ownRecallPercentage = (ownRecall * 100).toFixed(2) + '%';
    }

    // Function to get the mean overall sentiment
    async function getMeanSent() {
        const mean_sent = await provider.getMeanOverallSentiment();
        vaderSentMean = sliceString(mean_sent['mean_vs_sent'].toString());
        lrcSentOtherMean = sliceString(mean_sent['mean_lrc_other_sent'].toString());
        lrcSentOwnMean = sliceString(mean_sent['mean_lrc_own_sent'].toString());
        bertSentMean = sliceString(mean_sent['mean_bert_sent'].toString());
    }

    // Function to execute the sentiment analysis for a custom tweet
    async function executeCustomTweetSent() {
        if (userTweet) {
            const scores = await provider.getSentimentTweet(userTweet);
            [vaderSent, sgdSentOther, sgdSentOwn, bertSent] = scores.map(score => sliceString(score.toString()));
        }
    }

    // Function to slice strings such that all sentiment values have the same amount of decimal places
    const sliceString = (str: string) => {
        if (str[0] === '-') {
            return str.slice(0, 7);
        }
        return str.slice(0, 6);
    };

    onMount(() => {
        // Fill the mean sent, topic sent and trained model performance values on mount
        getMeanSent();
        getTrainedModelPerf();
        getSentimentByTopic();
    })

</script>


<title>Text Analytics - Sentiment Analysis</title>
<h1>Sentiment Analysis</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Sentiment</BreadcrumbItem>
</Breadcrumb>


<div>
    <FormGroup>
        <Form>
            <h4 in:fly={{ x: 400, duration: transDuration, delay: 200 }}>Welcome!</h4>
            <p in:fly={{ x: 400, duration: transDuration, delay: 200 }}>to the Sentiment Analysis page! Here, you can
                view
                sentiment analysis of tweets,
                but you can also input your own "tweet" to see what sentiment it conveys. Furthermore, you can see
                sentiment analysis by country and track sentiment changes over time. Get an in-depth understanding of
                the buzz surrounding the World Cup with this sentiment analysis tool.</p>
            <h4 in:fly={{ x: 400, duration: transDuration, delay: 200 }}>Overall sentiment</h4>
            <p in:fly={{ x: 400, duration: transDuration, delay: 200 }}>Below, you can take a look at the average
                sentiment over all tweets by each method. Each method will
                link to some documentation. To learn more about the methods, please check out the last section.</p>
            <div in:fly={{ x: 400, duration: transDuration, delay: 200 }}>
                <Row>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 600 }}>
                            <Alert color="primary">
                                <h5><a href="https://github.com/cjhutto/vaderSentiment">vaderSentiment</a></h5>
                                {vaderSentMean}
                            </Alert>
                        </div>
                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 700 }}>
                            <Alert color="warning">
                                <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOther</a></h5>
                                {lrcSentOtherMean}
                            </Alert>
                        </div>

                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 800 }}>
                            <Alert color="success">
                                <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOtherOwn</a></h5>
                                {lrcSentOwnMean}
                            </Alert>
                        </div>
                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 900 }}>
                            <Alert color="danger">
                                <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT
                                    based
                                    Classifier</a></h5>
                                {bertSentMean}
                            </Alert>
                        </div>
                    </Col>
                </Row>
            </div>
        </Form>

        <Form>
            <div in:fly={{ y: 400, duration: transDuration*1.5, delay: 1500 }}>
                <h4>Try it out!</h4>
                <p>Below, you can write your own 'Tweet' and let it be rated by our classifiers. Don't be surprised if
                    some of our classifiers return 0 if an input is likely neutral!</p>
                <Row>
                    <Col xs="12" sm="9">
                        <FormGroup label="Enter your Tweet">
                            <Input
                                    bind:value={userTweet}
                            />
                        </FormGroup>
                    </Col>
                    <Col>
                        <FormGroup>
                            <Button type="button" on:click={executeCustomTweetSent}>Perform Sentiment Analysis</Button>
                        </FormGroup>
                    </Col>
                </Row>

                <Row>
                    <Col>
                        <Alert color="primary">
                            <h5><a href="https://github.com/cjhutto/vaderSentiment">vaderSentiment</a></h5>
                            {vaderSent}
                        </Alert>
                    </Col>
                    <Col>
                        <Alert color="warning">
                            <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOther</a></h5>
                            {sgdSentOther}
                        </Alert>
                    </Col>
                    <Col>
                        <Alert color="success">
                            <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOwn</a></h5>
                            {sgdSentOwn}
                        </Alert>
                    </Col>
                    <Col>
                        <Alert color="danger">
                            <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT
                                based
                                Classifier</a></h5>
                            {bertSent}
                        </Alert>
                    </Col>
                </Row>
            </div>
        </Form>

        <Form>
            <div in:fly={{ y: 400, duration: transDuration*1.5, delay: 1500 }}>

                <h4>Sentiment over time</h4>
                <p>Below, you can take a look at the average sentiment over time. You are able so sort by days, weeks or
                    months and decide which methods you would like to see. The amount of tweets for a given time period
                    can be seen in the background as a bar chart.</p>

                <Row>
                    <SentimentByCard
                            header="Sentiment over time by different methods"
                            footer="This graph clearly shows"
                    >
                    </SentimentByCard>
                </Row>
            </div>
        </Form>

        <Form>
            <p></p>
            <h4>Sentiment by topic</h4>
            <p>Below, you can take a look at the average sentiment by different topics that we identified in our corpus.
            </p>

            <FormGroup>
                <Input
                        id="showdetailstopicsent"
                        type="checkbox"
                        label="Show Details"
                        bind:checked={showTopicSentDetails}
                />
            </FormGroup>
            <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
                {#each Array(11) as _, i}
                    <Col>
                        {#if topics_mean[i] >= 0.1}
                            <Alert color="success">
                                <h5 style="color: black">{titles[i]}</h5>
                                Mean: {topics_mean[i]}
                                {#if showTopicSentDetails}
                                    <hr>
                                    <br>
                                    vaderSentiment: {topics_vs_sent[i]}
                                    <br>
                                    SGDClassifierOther: {topics_lrc_other[i]}
                                    <br>
                                    SGDClassifierOwn: {topics_lrc_own[i]}
                                    <br>
                                    BERT based Classifier: {topics_bert_sent[i]}
                                    <br>
                                    Based on: {topics_count[i]} Tweets
                                {/if}
                            </Alert>
                        {:else if topics_mean[i] >= 0}
                            <Alert color="warning">
                                <h5 style="color: black">{titles[i]}</h5>
                                Mean: {topics_mean[i]}
                                {#if showTopicSentDetails}
                                    <hr>
                                    <br>
                                    vaderSentiment: {topics_vs_sent[i]}
                                    <br>
                                    SGDClassifierOther: {topics_lrc_other[i]}
                                    <br>
                                    SGDClassifierOwn: {topics_lrc_own[i]}
                                    <br>
                                    BERT based Classifier: {topics_bert_sent[i]}
                                    <br>
                                    Based on: {topics_count[i]} Tweets
                                {/if}
                            </Alert>
                        {:else}
                            <Alert color="danger">
                                <h5 style="color: black">{titles[i]}</h5>
                                Mean: {topics_mean[i]}
                                {#if showTopicSentDetails}
                                    <hr>
                                    <br>
                                    vaderSentiment: {topics_vs_sent[i]}
                                    <br>
                                    SGDClassifierOther: {topics_lrc_other[i]}
                                    <br>
                                    SGDClassifierOwn: {topics_lrc_own[i]}
                                    <br>
                                    BERT based Classifier: {topics_bert_sent[i]}
                                    <br>
                                    Based on: {topics_count[i]} Tweets
                                {/if}
                            </Alert>
                        {/if}
                    </Col>
                {/each}
            </Row>
        </Form>

        <Form>
            <p></p>
            <h4>Evaluation and Limitations of our Trained Sentiment Models</h4>
            <p>In order to assess the sentiment of the tweets we obtained, we utilized two methods that do not require
                further training. The first method is the 'vaderSentiment' analyzer, which is specifically designed to
                work with social media data and was found to be a suitable choice. The second method is a BERT-based
                model that was trained on a corpus of 129 million tweets.
            </p>
            <p>Additionally, we developed our own sentiment analyzers using logistic regression (SGDClassifier from
                sklearn.linear_models). These analyzers were trained on two datasets: a pre-existing dataset of 26,000
                labeled tweets and a smaller dataset of approximately 1,000 tweets that we manually labeled. The latter
                dataset represents a limitation of the models.
            </p>
            <p>The performance of our models is reported in terms of accuracy, recall, and F1 score.
            </p>
            <h5>SGD Classifier with 'other' dataset</h5>
            <Row>
                <Col>
                    <Alert color="success">
                        <h5 style="color: black">Accuracy</h5>
                        {otherAccuracyPercentage}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5 style="color: black">Recall</h5>
                        {otherRecallPercentage}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5 style="color: black">F1</h5>
                        {otherF1Percentage}
                    </Alert>
                </Col>

            </Row>
            <h5>SGD Classifier with own dataset</h5>
            <Row>
                <Col>
                    <Alert color="danger">
                        <h5 style="color: black">Accuracy</h5>
                        {ownAccuracyPercentage}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        <h5 style="color: black">Recall</h5>
                        {ownRecallPercentage}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5 style="color: black">F1</h5>
                        {ownF1Percentage}
                    </Alert>
                </Col>

            </Row>
        </Form>

    </FormGroup>
</div>