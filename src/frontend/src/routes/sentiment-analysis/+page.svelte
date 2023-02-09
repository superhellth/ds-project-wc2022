<script lang="ts">
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {Alert, Breadcrumb, BreadcrumbItem, Button, Col, Form, FormGroup, Input, Label, Row} from "sveltestrap";
    import {onMount} from "svelte";
    import ChartCard from "../../svelte-components/ChartCard.svelte";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();

    // Overall Sentiment variables
    let userTweet: string = '';
    let vaderSentMean = 'Loading...';
    let lrcSentOtherMean = 'Loading...';
    let lrcSentOwnMean = 'Loading ...';
    let bertSentMean = 'Loading ...';

    // Try it out variables
    let vaderSent = 'Waiting...'; // variable to hold the vaderSent score
    let sgdSentOther = 'Waiting...'; // variable to hold the trainedSent score
    let sgdSentOwn = 'Waiting...'; // variable to hold the nbSent score
    let bertSent = "Waiting... (BERT: I\'m a bit slow, sorry!)"; // variable to hold the bertSent score

    // Sentiment by date variables
    let useVaderSent = true;
    let useSgdSentOther = false;
    let useSgdSentOwn = false;
    let useBertSent = false;

    // Trained model performance variables
    let lrcAccOther = 'Waiting...';
    let lrcRecOther = 'Waiting...';
    let lrcF1Other = 'Waiting...';
    let lrcF1Own = 'Waiting...';
    let lrcAccOwn = 'Waiting...';
    let lrcRecOwn = 'Waiting...';


    async function getTrainedModelPerf() {
        const performance = await provider.getTrainedModelPerformance();
        lrcAccOther = performance[0].toString().slice(0, 4);
        lrcRecOther = performance[1].toString().slice(0, 4);
        lrcF1Other = performance[2].toString().slice(0, 4);
        lrcF1Own = performance[3].toString().slice(0, 4);
        lrcAccOwn = performance[4].toString().slice(0, 4);
        lrcRecOwn = performance[5].toString().slice(0, 4);
    }


    async function getMeanSent() {
        const mean_sent = await provider.getMeanOverallSentiment();
        vaderSentMean = mean_sent['mean_vs_sent'].toString().slice(0, 8);
        lrcSentOtherMean = mean_sent['mean_lrc_other_sent'].toString().slice(0, 8);
        lrcSentOwnMean = mean_sent['mean_lrc_own_sent'].toString().slice(0, 8);
        bertSentMean = mean_sent['mean_bert_sent'].toString().slice(0, 8);
    }

    async function executeCustomTweetSent() {
        if (userTweet) {
            const scores = await provider.getSentimentTweet(userTweet)
            vaderSent = scores[0].toString().slice(0, 8);
            sgdSentOther = scores[1].toString().slice(0, 8);
            sgdSentOwn = scores[2].toString().slice(0, 8);
            bertSent = scores[3].toString().slice(0, 8);
        }
    }

    onMount(() => {
        getMeanSent();
        getTrainedModelPerf();
    })

    function redraw_graph() {
        console.log("Redrawing graph with methods X and Y...")
    }



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
            <h4>Welcome!</h4>
            <p>to the Sentiment Analysis page! Here, you can view sentiment analysis of tweets,
                but you can also input your own "tweet" to see what sentiment it conveys. Furthermore, you can see
                sentiment analysis by country and track sentiment changes over time. Get an in-depth understanding of
                the buzz surrounding the World Cup with this sentiment analysis tool.</p>
            <h4>Overall sentiment</h4>
            <p>Below, you can take a look at the average sentiment over all tweets by each method. Each method will
            link to some documentation.</p>
            <Row>
                <Col>
                    <Alert color="primary">
                        <h5><a href="https://github.com/cjhutto/vaderSentiment">vaderSentiment</a></h5>
                        {vaderSentMean}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOther</a></h5>
                        {lrcSentOtherMean}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifierOtherOwn</a></h5>
                        {lrcSentOwnMean}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT based Classifier</a></h5>
                        {bertSentMean}
                    </Alert>
                </Col>
            </Row>
        </Form>

        <Form>
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
                        <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT based Classifier</a></h5>
                        {bertSent}
                    </Alert>
                </Col>
            </Row>
        </Form>

        <Form>
            <h4>Sentiment over time</h4>
            <p>Below, you can take a look at the average sentiment over time. You are able so sort by timeframe and
            decide which methods you would like to see.</p>
            <div class="float-left">
                <Row>
                <Col>
                    <FormGroup style="margin-left: 2em">
                        <Label for="timeframe-select"><b>Timeframe selection</b></Label>
                        <Input
                            type="select"
                            id="timeframe-select"
                        >
                        {#each ["by Day", "by Week", "by Month"] as timeframe}
                            <option>{timeframe}</option>
                        {/each}
                    </Input>
                    </FormGroup>
                </Col>
                <Col>
                    <b>Sentiment methods</b>
                    <Row>
                          <FormGroup>
                            <Input
                                    id="cvs"
                                    type="checkbox"
                                    label="vaderSentiment"
                                    bind:value={useVaderSent}
                                    on:change={redraw_graph()}
                            />
                          </FormGroup>
                    </Row>
                    <Row>
                          <FormGroup>
                            <Input
                                    id="ccother"
                                    type="checkbox"
                                    label="SGDClassifierOther"
                                    bind:value={useSgdSentOther}
                                    on:change={redraw_graph()}

                            />
                          </FormGroup>
                    </Row>
                    <Row>
                          <FormGroup>
                            <Input
                                    id="ccown"
                                    type="checkbox"
                                    label="SGDClassifierOwn"
                                    bind:value={useSgdSentOwn}
                                    on:change={redraw_graph()}
                            />
                          </FormGroup>
                    </Row>
                    <Row>
                          <FormGroup>
                            <Input
                                    id="cbc"
                                    type="checkbox"
                                    label="BERT based Classifier"
                                    bind:value={useBertSent}
                                    on:change={redraw_graph()}
                            />
                          </FormGroup>
                    </Row>
                </Col>
                </Row>

            </div>

            <Row>
                <ChartCard header="Sentiment over time" footer="As you can see...">
                </ChartCard>
            </Row>

        </Form>

        <Form>
            <p></p>
            <h4>Sentiment by topic</h4>
            <p>Below, you can take a look at the average sentiment by different topics that we identified in our corpus.
            </p>

            <Row>
                <Col>
                    <Alert color="primary">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        Topic X
                    </Alert>
                </Col>
            </Row>
            <Row>
                <Col>
                    <Alert color="success">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        Topic X
                    </Alert>
                </Col>
                <Col>
                    <Alert color="primary">
                        Topic X
                    </Alert>
                </Col>
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
                        <h5>Accuracy</h5>
                        {lrcAccOther}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5>Recall</h5>
                        {lrcRecOther}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5>F1</h5>
                        {lrcF1Other}
                    </Alert>
                </Col>

            </Row>
            <h5>SGD Classifier with own dataset</h5>
            <Row>
                                <Col>
                    <Alert color="danger">
                        <h5>Accuracy</h5>
                        {lrcAccOwn}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        <h5>Recall</h5>
                        {lrcRecOwn}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5>F1</h5>
                        {lrcF1Own}
                    </Alert>
                </Col>

            </Row>
        </Form>

    </FormGroup>
</div>