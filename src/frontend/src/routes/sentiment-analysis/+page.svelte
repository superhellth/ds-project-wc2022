<script lang="ts">
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {Alert, Breadcrumb, BreadcrumbItem, Button, Col, Form, FormGroup, Input, Row, Tooltip} from "sveltestrap";
    import {onMount} from "svelte";
    import SentimentByCard from "../../svelte-components/SentimentByCard.svelte";
    import {fly} from "svelte/transition";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();

    // Overall Sentiment variables
    let userTweet: string = '';
    let vaderSentMean: string = 'Loading...';
    let lrcSentOtherMean: string = 'Loading...';
    let lrcSentOwnMean: string = 'Loading ...';
    let bertSentMean: string = 'Loading ...';

    // Try it out variables
    let vaderSent: string = 'Waiting...';
    let sgdSentOther: string = 'Waiting...';
    let sgdSentOwn: string = 'Waiting...';
    let bertSent: string = "Waiting...";

    // Trained model performance variables
    let otherAccuracyPercentage: string = 'Waiting...';
    let otherRecallPercentage: string = 'Waiting...';
    let otherF1Percentage: string = 'Waiting...';
    let ownF1Percentage: string = 'Waiting...';
    let ownAccuracyPercentage: string = 'Waiting...';
    let ownRecallPercentage: string = 'Waiting...';

    // Sent by topic variables
    const topics_mean: string[] = Array(11).fill('Waiting...');
    const topics_vs_sent: string[] = Array(11).fill('Waiting...');
    const topics_bert_sent: string[] = Array(11).fill('Waiting...');
    const topics_lrc_other: string[] = Array(11).fill('Waiting...');
    const topics_lrc_own: string[] = Array(11).fill('Waiting...');
    const topics_count: string[] = Array(11).fill('Waiting...');
    const titles: string[] = [
        'The Center Cluster', '#Cluster', '#SayTheirNames',
        'C\'mon England!', '???', 'Steve Harvey',
        'SUIIII!!!', 'NFT and Crypto', '你好中国人！',
        'Cluster 10', 'Stand with Ukraine'
    ];
    let showTopicSentDetails: boolean = false;

    // Add qatar sentiment variables
    let qatarSentiment = {
        before: Array(8).fill("Waiting..."),
        during: Array(8).fill("Waiting..."),
        after: Array(8).fill("Waiting..."),
    };

    let qatarAmountTweets = {
        before: 10000,
        during: 100000,
        after: 10000
    }

    let bertQatarT: number;
    let vsQatarT: number;

    // Add transition variables
    let transDuration: number = 600;

    // Function to get sentiment towards qatar over time
    async function getQatarSentiment() {
        const data = await provider.getQatarSentiment();

        const keys = ['before', 'during', 'after'];
        keys.forEach(key => {
            const vs_sent = data[key]['vs_sent'];
            const lrc_other = data[key]['lrc_other'];
            const lrc_own = data[key]['lrc_own'];
            const bert_sent = data[key]['bert_sent'];

            qatarSentiment[key][0] = sliceString(vs_sent[0].toString());
            qatarSentiment[key][1] = sliceString(vs_sent[1].toString());
            qatarSentiment[key][2] = sliceString(lrc_other[0].toString());
            qatarSentiment[key][3] = sliceString(lrc_other[1].toString());
            qatarSentiment[key][4] = sliceString(lrc_own[0].toString());
            qatarSentiment[key][5] = sliceString(lrc_own[1].toString());
            qatarSentiment[key][6] = sliceString(bert_sent[0].toString());
            qatarSentiment[key][7] = sliceString(bert_sent[1].toString());
        });

        qatarAmountTweets['before'] = data['before']['amount']
        qatarAmountTweets['during'] = data['during']['amount']
        qatarAmountTweets['after'] = data['after']['amount']

        bertQatarT = (qatarSentiment['after'][6] - qatarSentiment['before'][6]) / (Math.sqrt(
            (qatarSentiment['after'][7] / qatarAmountTweets['after']) + (qatarSentiment['before'][7] / qatarAmountTweets['before'])
        ))

        vsQatarT = (qatarSentiment['after'][0] - qatarSentiment['before'][0]) / (Math.sqrt(
            (qatarSentiment['after'][1] / qatarAmountTweets['after']) + (qatarSentiment['before'][1] / qatarAmountTweets['before'])
        ))
    }

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
        const mean_sent: any = await provider.getMeanOverallSentiment();
        vaderSentMean = sliceString(mean_sent['mean_vs_sent'].toString());
        lrcSentOtherMean = sliceString(mean_sent['mean_lrc_other_sent'].toString());
        lrcSentOwnMean = sliceString(mean_sent['mean_lrc_own_sent'].toString());
        bertSentMean = sliceString(mean_sent['mean_bert_sent'].toString());
    }

    // Function to execute the sentiment analysis for a custom tweet
    async function executeCustomTweetSent() {
        if (userTweet) {
            const scores: any = await provider.getSentimentTweet(userTweet);
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

    let MathJax;
    let H0 = "$$ H_0: \\mu_{after} - \\mu_{before} = 0 $$";
    let H1 = "$$ H_1: \\mu_{after} - \\mu_{before} \\neq 0 $$";
    let p = '\\(p = 0.01\\)';
    let T = "$$T = \\frac{\\mu_{after} - \\mu_{before}}{\\sqrt{\\frac{\\sigma^2_{after}}{n_{after}} + \\frac{\\sigma^2_{before}}{n_{before}}}}$$";
    let Tbert = "\\(T_{bert} = \\)";
    let Tvs = "\\(T_{vs} = \\)";
    let z = "\\(\\varphi(0.99) = 2.5758\\)";

    onMount(() => {
        // Fill the mean sent, topic sent and trained model performance values on mount
        getMeanSent();
        getTrainedModelPerf();
        getSentimentByTopic();
        getQatarSentiment();
        let script = document.createElement('script');
        script.src = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js";
        document.head.append(script);

        script.onload = () => {
            MathJax = {
                tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]},
                svg: {fontCache: 'global'}
            };
        };
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
                view sentiment analysis of tweets,
                but you can also input your own "tweet" to see what sentiment it conveys. Furthermore, you can see
                sentiment analysis by topic and track sentiment changes over time. Get an in-depth understanding of
                the buzz surrounding the World Cup with this sentiment analysis tool.</p>
            <h4 in:fly={{ x: 400, duration: transDuration, delay: 200 }}>Overall sentiment</h4>
            <p in:fly={{ x: 400, duration: transDuration, delay: 200 }}>Below, you can take a look at the average
                sentiment over all tweets by each method. Each method title will
                link to some documentation. To learn more about the methods, please hover over the blocks or check out
                the last section.</p>
            <div in:fly={{ x: 400, duration: transDuration, delay: 200 }}>
                <Row>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 600 }}>
                            <Alert color="primary" id="vader-sent-alert-id">
                                <h5><a href="https://github.com/cjhutto/vaderSentiment">vaderSentiment</a></h5>
                                {vaderSentMean}
                            </Alert>
                            <Tooltip placement="bottom" target="vader-sent-alert-id">
                                This score was calculated by the SentimentIntensityAnalyzer class of the vaderSentiment
                                library.
                                It uses a 'lexicon' and 'rule-based' approach and is fine-tuned for social media
                                sentiment analysis.
                            </Tooltip>
                        </div>
                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 700 }}>
                            <Alert color="primary" id="other-sent-alert-id">
                                <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOther</a></h5>
                                {lrcSentOtherMean}
                            </Alert>
                            <Tooltip placement="bottom" target="other-sent-alert-id">
                                This sentiment score is calculated by the
                                sklearn.SGDClassifier class in combination with
                                a TfidfVectorizer. It trained using a file with
                                26000 labeled tweets which can be found in our
                                repository under 'src/data/sentiment-data/Tweets_train.csv'.
                            </Tooltip>
                        </div>

                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 800 }}>
                            <Alert color="primary" id="own-sent-alert-id">
                                <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOtherOwn</a></h5>
                                {lrcSentOwnMean}
                            </Alert>
                            <Tooltip placement="bottom" target="own-sent-alert-id">
                                This sentiment score is calculated by the
                                sklearn.SGDClassifier class in combination with
                                a TfidfVectorizer. It trained using a file with
                                1000 self-labeled tweets from our dataset which can be found in our
                                repository under 'src/data/sentiment-data/classification_with_text_train.csv'.
                            </Tooltip>
                        </div>
                    </Col>
                    <Col>
                        <div in:fly={{ x: 400, duration: transDuration*1.5, delay: 900 }}>
                            <Alert color="primary" id="bert-sent-alert-id">
                                <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT
                                    based
                                    Classifier</a></h5>
                                {bertSentMean}
                            </Alert>
                            <Tooltip placement="bottom" target="bert-sent-alert-id">
                                This sentiment score is calculated by the
                                'distilbert-base-uncased-finetuned-sst-2-english'
                                model as found on HuggingFace. In order
                                for the tweets to be processed 'properly' we
                                looked at the training data for that model. To
                                keep our input similar we decided to drop for example all
                                non-ascii symbols. We did not fine-tune the model.
                            </Tooltip>
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
                        <Alert color="primary">
                            <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOther</a></h5>
                            {sgdSentOther}
                        </Alert>
                    </Col>
                    <Col>
                        <Alert color="primary">
                            <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOwn</a></h5>
                            {sgdSentOwn}
                        </Alert>
                    </Col>
                    <Col>
                        <Alert color="primary">
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

        <Form>
            <p></p>
            <h4>Results</h4>
            <p>
                After all that analysis one question still remains. Did Qatar succeed in 'sportwashing'? Were they able
                to make people look past the human rights abuse and buy into the illusion?
            </p>
            <p>
                To definitively answer that question is very hard because it involves a lot of factors. There are many
                reasons why the sentiment towards Qatar might have changed during the World Cup. Maybe the constant
                scandals involving the iranian government took some heat of Qatar? Maybe the sentiment didn't change?
                Or maybe people really fell for it?
            </p>
            <p>
                Let's first take a look at the following three values as they show the sentiment of all Tweets that
                mention 'qatar' before, during and after the World Cup.
            </p>
            <h5>'Qatar' mentions before, during and after the World Cup</h5>

            <Row>
                <Col>
                    <Alert color="danger">
                        <h5 style="color: black">Before</h5>
                        <b>vaderSentiment</b>:
                        <br>
                        Mean: {qatarSentiment['before'][0]}
                        <br>
                        SD: {qatarSentiment['before'][1]}
                        <br>
                        <b>SGDClassifierOther</b>:
                        <br>
                        Mean: {qatarSentiment['before'][2]}
                        <br>
                        SD: {qatarSentiment['before'][3]}
                        <br>
                        <b>SGDClassifierOwn</b>:
                        <br>
                        Mean: {qatarSentiment['before'][4]}
                        <br>
                        SD: {qatarSentiment['before'][5]}
                        <br>
                        <b>BERT based Classifier</b>:
                        <br>
                        Mean: {qatarSentiment['before'][6]}
                        <br>
                        SD: {qatarSentiment['before'][7]}
                        <br>
                        <b>Amount Tweets</b>: {qatarAmountTweets['before']}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5 style="color: black">During</h5>
                        <b>vaderSentiment</b>:
                        <br>
                        Mean: {qatarSentiment['during'][0]}
                        <br>
                        SD: {qatarSentiment['during'][1]}
                        <br>
                        <b>SGDClassifierOther</b>:
                        <br>
                        Mean: {qatarSentiment['during'][2]}
                        <br>
                        SD: {qatarSentiment['during'][3]}
                        <br>
                        <b>SGDClassifierOwn</b>:
                        <br>
                        Mean: {qatarSentiment['during'][4]}
                        <br>
                        SD: {qatarSentiment['during'][5]}
                        <br>
                        <b>BERT based Classifier</b>:
                        <br>
                        Mean: {qatarSentiment['during'][6]}
                        <br>
                        SD: {qatarSentiment['during'][7]}
                        <br>
                        <b>Amount Tweets</b>: {qatarAmountTweets['during']}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5 style="color: black">After</h5>
                        <b>vaderSentiment</b>:
                        <br>
                        Mean: {qatarSentiment['after'][0]}
                        <br>
                        SD: {qatarSentiment['after'][1]}
                        <br>
                        <b>SGDClassifierOther</b>:
                        <br>
                        Mean: {qatarSentiment['after'][2]}
                        <br>
                        SD: {qatarSentiment['after'][3]}
                        <br>
                        <b>SGDClassifierOwn</b>:
                        <br>
                        Mean: {qatarSentiment['after'][4]}
                        <br>
                        SD: {qatarSentiment['after'][5]}
                        <br>
                        <b>BERT based Classifier</b>:
                        <br>
                        Mean: {qatarSentiment['after'][6]}
                        <br>
                        SD: {qatarSentiment['after'][7]}
                        <br>
                        <b>Amount Tweets</b>: {qatarAmountTweets['after']}
                    </Alert>
                </Col>
            </Row>
            <p>
                Given the limitations of our own trained models we will focus on the other two methods to answer this
                question. The results couldn't be more clear. The two methods which are fine tuned for social media
                sentiment analysis come to the same conclusion:
            </p>
            <h4 style="text-align: center">
                Qatar's sportswashing (seems to have) worked!
            </h4>
            <p>
                Both methods show a significant increase in sentiment after the world cup! (Of course this could be the
                result of something that has nothing to do with Qatar, as mentioned before.) But is it really
                significant?
                Well, this gives me the opportunity to get out my old statistics book and check. Here we go:
            </p>
            <p>
                To confirm that the test result is actually significant, we have to pick a significance level and
                two hypotheses. The null-hypothesis will be that the values do not differ. The alternative hypotheses
                will be that the means will differ. (Please reload the page once if the math does not render correctly!).
            </p>
            <p>
                {H0}
            </p>
            <p>
                {H1}
            </p>
            <p>
                Let's pick {p} because, why not. Then we write down the test statistic for the tests:
                {T}
                <br>
                Plugging in the values we get:
                <br>
                {Tbert} {bertQatarT}
                <br>
                and
                <br>
                {Tvs} {vsQatarT}
            </p>
            <p>
                As we can see, both values are way larger than the required {z} we needed in order to say the
                findings are significant.
            </p>
        </Form>
    </FormGroup>
</div>