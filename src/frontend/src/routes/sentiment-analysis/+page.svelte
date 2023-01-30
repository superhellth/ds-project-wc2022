<script lang="ts">
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { onMount } from "svelte";
    import {Alert, Button, CardText, Col, Form, FormGroup, Input, Row, Tooltip} from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();

    let userTweet: string = '';
    let vaderSent = 'Waiting...'; // variable to hold the vaderSent score
    let trainedSent = 'Waiting...'; // variable to hold the trainedSent score
    let nbSent = 'Waiting...'; // variable to hold the nbSent score
    let bertSent = "Waiting... (BERT: I\'m a bit slow, sorry!)"; // variable to hold the bertSent score

    async function executeCustomTweetSent() {
        if (userTweet) {
            const scores = await provider.getSentimentTweet(userTweet)
            vaderSent = scores[0];
            trainedSent = scores[1];
            nbSent = scores[2];
            bertSent = scores[3];
        }
    }

</script>

<title>Text Analytics - Sentiment Analysis</title>

<div>
    <FormGroup>
        <Form>
            <h3>Sentiment Analysis</h3>
            <p>Welcome to the Sentiment Analysis page! Here, you can view sentiment analysis of tweets,
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
                        0.156459156(dummy)
                    </Alert>
                </Col>
                <Col>
                    <Alert color="warning">
                        <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifier</a></h5>
                        0.156459156(dummy)
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5><a href="https://scikit-learn.org/stable/index.html">Naive Bayes Classifier</a></h5>
                        0.156459156(dummy)
                    </Alert>
                </Col>
                <Col>
                    <Alert color="danger">
                        <h5><a href="https://huggingface.co/distilbert-base-uncased-finetuned-sst-2-english">BERT based Classifier</a></h5>
                        0.156459156(dummy)
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
                    <FormGroup floating label="Enter your Tweet">
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
                        <h5><a href="https://scikit-learn.org/stable/index.html">SGDClassifier</a></h5>
                        {trainedSent}
                    </Alert>
                </Col>
                <Col>
                    <Alert color="success">
                        <h5><a href="https://scikit-learn.org/stable/index.html">Naive Bayes Classifier</a></h5>
                        {nbSent}
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
    </FormGroup>
</div>
