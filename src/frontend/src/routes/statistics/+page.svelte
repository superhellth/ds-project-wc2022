<script lang="ts">
    import BarChartCard from "src/svelte-components/MapChartCard.svelte";
    import TweetCountGraph from "src/svelte-components/DateHistogramCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Breadcrumb, BreadcrumbItem, Col, Row } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let authorLocationMap: Promise<Map<string, number>> =
        provider.getTermHistogram("author.location", 20);
    let authorVerifiedMap: Promise<Map<string, number>> =
        provider.getTermHistogram("author.verified", 10);
    let authorMap: Promise<Map<string, number>> = provider.getTermHistogram(
        "author.username",
        10
    );
    let possiblySensitiveMap: Promise<Map<string, number>> =
        provider.getTermHistogram("possibly_sensitive", 10);
</script>

<title>Statistics - Collected Data</title>
<h1>Corpus Statistics</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Statistics</BreadcrumbItem>
</Breadcrumb>

<Row>
    <Col>
        <TweetCountGraph
            header="Tweets by Day"
            footer="This graph shows quite well the biggest flaw of our data. Since we tried collecting every single Tweet matching our Query, instead of sampling, we ran into the issue of being limited by the Twitter-Api Tweet limit, which is 2.000.000 per Month. Thus there are some days in which we did not collect any data. In total there are 15 days for which we have no Tweets at all and additionally there are 3 days for which we did not collect all Tweets we could have."
            field="created_at"
            interval="day"
            chart_id="c1"
        />
    </Col>
    <Col>
        <TweetCountGraph
            header="Tweets by Account ages"
            footer="This is an interesting distribution because as you can see there are unproportionally many Tweets from Accounts created in 2022. This could be explained by two things. On one hand people could have been so excited for the world cup, they decided to create an account especially to tweet about this event. However even if there are cases in which this was the case, it does not explain this large of a discrepancy. So on the other hand it is very likely that this is caused by spam/scam accounts. We think that many people took the opportunity of an event this big to create countless spam accounts to push crypto and other scams."
            field="author.created_at"
            interval="year"
            chart_id="c2"
        />
    </Col>
</Row>
<Row>
    <Col>
        {#await authorMap}
            <Loading displayString="Authors" />
        {:then map}
            <BarChartCard
                header="Tweets by Author"
                footer="Lorem ipsum"
                chartID="d3"
                dataMap={map}
                type="bar"
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
                type="bar"
            />
        {/await}
    </Col>
</Row>
<Row>
    <Col>
        {#await possiblySensitiveMap}
            <Loading displayString="possibly sensitive tweets" />
        {:then map}
            <BarChartCard
                header="Possibly sensitive Tweets"
                footer="yes yes"
                chartID="d4"
                dataMap={map}
                type="pie"
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
