<script lang="ts">
    import { Col, Row } from "sveltestrap";
    import TweetCountGraph from "src/svelte-components/DateHistogramCard.svelte";
</script>

<title>Statistics - Collected Data</title>

<Row>
    <Col>
        <TweetCountGraph header="Tweets by Day" footer="bal bla bla" field="created_at" interval="day" chart_id="c1" />
    </Col>
    <Col>
        <TweetCountGraph header="Tweets by Account ages" footer="bal bla bla" field="author.created_at" interval="year" chart_id="c2" />
    </Col>
</Row>