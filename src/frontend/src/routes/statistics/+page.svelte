<script lang="ts">
    import BarChartCard from "src/svelte-components/MapChartCard.svelte";
    import TweetCountGraph from "src/svelte-components/DateHistogramCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Col, Row } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let authorLocationMap: Promise<Map<string, number>> =
        provider.getTermHistogram("author.location", 10);
    let authorVerifiedMap: Promise<Map<string, number>> =
        provider.getTermHistogram("author.verified", 10);
    let authorMap: Promise<Map<string, number>> = provider.getTermHistogram(
        "author.username",
        10
    );
</script>

<title>Statistics - Collected Data</title>

<Row>
    <Col>
        <TweetCountGraph
            header="Tweets by Day"
            footer="bal bla bla"
            field="created_at"
            interval="day"
            chart_id="c1"
        />
    </Col>
    <Col>
        <TweetCountGraph
            header="Tweets by Account ages"
            footer="bal bla bla"
            field="author.created_at"
            interval="year"
            chart_id="c2"
        />
    </Col>
</Row>
<Row>
    <Col>
        {#await authorMap}
            <Loading displayString="Author Verifications" />
        {:then map}
            <BarChartCard
                header="Tweets by Author"
                footer="Lorem ipsum"
                chartID="d3"
                dataMap={map}
            />
        {/await}
    </Col>
    <Col>
        {#await authorLocationMap}
            <Loading displayString="Author Locations" />
        {:then map}
            <BarChartCard
                header="Tweets by location"
                footer="yes yes"
                chartID="d1"
                dataMap={map}
            />
        {/await}
    </Col>
    <Col>
        {#await authorVerifiedMap}
            <Loading displayString="Author Verifications" />
        {:then map}
            <BarChartCard
                header="Tweets by Author Verifications"
                footer="Lorem ipsum"
                chartID="d2"
                dataMap={map}
                type="pie"
            />
        {/await}
    </Col>
</Row>
