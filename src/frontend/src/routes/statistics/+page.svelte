<script lang="ts">
    import TweetCountGraph from "src/svelte-components/DateHistogramCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import BarChartCard from "src/svelte-components/MapChartCard.svelte";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {Breadcrumb, BreadcrumbItem, Col, Row} from "sveltestrap";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();
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
    let authorAgeMap: Map<string, number> = new Map<string, number>();
    let authorVerificationMap: Map<string, number> = new Map<string, number>();

    let authorAgeQuery = `{
        "size": 0,
        "aggs": {
            "authors_per_year": {
                "date_histogram": {
                    "field": "author.created_at",
                    "interval": "year"
                },
                "aggs": {
                    "unique_authors": {
                        "cardinality": {
                            "field": "author.id"
                        }
                    }
                }
            }
        }
    }`;
    let authorVerificationQuery = `{
        "size": 0,
        "aggs": {
            "authors_by_verification": {
                "terms": {
                    "field": "author.verified",
                    "size": 2
                },
                "aggs": {
                    "unique_authors": {
                        "cardinality": {
                            "field": "author.id"
                        }
                    }
                }
            }
        }
    }`;

    let authorAgeResp = provider.queryESRaw(authorAgeQuery);
    let authorAgeMapIsReady: Promise<boolean> = prepareAuthorAgeMap();
    let authorVerificationResp = provider.queryESRaw(authorVerificationQuery);
    let authorVerificationMapIsReady: Promise<boolean> =
        prepareAuthorVerificationMap();

    async function prepareAuthorAgeMap() {
        let resp = await authorAgeResp;
        for (const [key, value] of Object.entries(
            resp.aggregations.authors_per_year.buckets
        )) {
            authorAgeMap.set(
                new Date(value.key_as_string).toLocaleDateString("short"),
                value.unique_authors.value
            );
        }
        return true;
    }

    async function prepareAuthorVerificationMap() {
        let resp = await authorVerificationResp;
        for (const [key, value] of Object.entries(
            resp.aggregations.authors_by_verification.buckets
        )) {
            authorVerificationMap.set(
                value.key_as_string,
                value.unique_authors.value
            );
        }
        return true;
    }
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
</Row>
<Row>
    <Col>
        {#await authorAgeMapIsReady}
            <Loading displayString="Account ages"/>
        {:then ignored}
            <BarChartCard
                    header="Authors by creation date"
                    footer="This is an interesting distribution because as you can see there are unproportionally many Tweets from Accounts created in 2022. This could be explained by two things. On one hand people could have been so excited for the world cup, they decided to create an account especially to tweet about this event. However even if there are cases in which this was the case, it does not explain this large of a discrepancy. So on the other hand it is very likely that this is caused by spam/scam accounts. We think that many people took the opportunity of an event this big to create countless spam accounts to push crypto and other scams."
                    chartID="d5"
                    dataMap={authorAgeMap}
                    type="bar"
                    valueLabel="Authors"
            />
        {/await}
    </Col>
    <Col>
        <TweetCountGraph
                header="Tweets by Account ages"
                footer="Now this is surprisingly unobtrusive. If the spike in accounts in 2022 was really explained by spam accounts we would expect the that the accounts created in 2022 tweeted a lot more than older accounts, since spam accounts tend to produce a lot more output than the average Twitter user. So perhaps there is another reason for the spike of account creations in 2022."
                field="author.created_at"
                interval="year"
                chart_id="c2"
        />
    </Col>
</Row>
<Row>
    <Col>
        {#await authorMap}
            <Loading displayString="Top Authors"/>
        {:then map}
            <BarChartCard
                    header="Tweets from the top 10 authors"
                    footer="This graph shows another interesting phenomenon about our corpus. There is a handful of Accounts like TVCooper that posted hundreds or even thousands of Tweets with a word cup hashtag, which is totally unrelated to the event. This causes some very unrelated topics to pop up in our topic modeling methods. Apart from TVCooper and AnkurRajvanshi3 the other accounts in this list are all news outlets and thus it's not surprising to see them have so many Tweets in our corpus."
                    chartID="d3"
                    dataMap={map}
                    type="bar"
            />
        {/await}
    </Col>
    <Col>
        {#await authorLocationMap}
            <Loading displayString="Author Locations"/>
        {:then map}
            <BarChartCard
                    header="Tweets by location"
                    footer="With this data we have to be careful. The great majority of our Tweets don't have location data at all and as you can even for the ones that have a location, the data is not too good, since places like 'UK' and 'London, England' are somewhat contradicting."
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
            <Loading displayString="possibly sensitive tweets"/>
        {:then map}
            <BarChartCard
                    header="Possibly sensitive Tweets"
                    footer="This graph is also to be considered carefully. It seems like not many of our Tweets are classified as 'possibly sensitive' but this is mainly due to the fact, that we collected the Tweets via a stream, that downloaded them, as soon as they were Tweeted and Twitter does not check Tweets before upload for sensitive content. Thus the actual amount of sensitve Tweets is actually much higher than stated here. Proof for that is the fact, that many Tweets we have in our corpus, which are not even labeled as possibly sensitve are now no longer available on the Twitter Website due to violationg the Twitter policies. A good example for that are the Tweets of AnkurRajvanish3 from the graph above."
                    chartID="d4"
                    dataMap={map}
                    type="pie"
            />
        {/await}
    </Col>

    <Col>
        {#await authorVerificationMapIsReady}
            <Loading displayString="Author verifications"/>
        {:then ignored}
            <BarChartCard
                    header="Author Verifications"
                    footer="We can't really evaluate this graph at the moment, because we have no data about the percentage of Twitter accounts verified outside our corpus. "
                    chartID="d6"
                    dataMap={authorVerificationMap}
                    type="pie"
                    valueLabel="Authors"
            />
        {/await}
    </Col>
    <Col>
        {#await authorVerifiedMap}
            <Loading displayString="Tweets by Author Verifications"/>
        {:then map}
            <BarChartCard
                    header="Tweets by Author Verifications"
                    footer="The fact that verified accounts tweeted more about the world cup, than non-verified ones is most likely caused by media accounts. As you can see from the top Accounts by number of Tweets, news sites loved to tweet about the world cup. And because many of these are verified, there are more Tweets per verified user, than per unverified user."
                    chartID="d2"
                    dataMap={map}
                    type="pie"
            />
        {/await}
    </Col>
</Row>
