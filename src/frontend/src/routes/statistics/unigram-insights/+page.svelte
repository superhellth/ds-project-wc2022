<script lang="ts">
    import CountTableCard from "src/svelte-components/CountTableCard.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Col, Row } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
</script>

<title>Statistics - Hashtags and Mentions</title>

<Row>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStopWords) => {
                return provider.getTopKUnigrams(
                    k,
                    includeStopWords,
                    false,
                    false
                );
            }}
            showStopWordSwitch={true}
            header="Common Tokens"
        />
    </Col>
</Row>
<Row>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKUnigrams(k, false, true, false);
            }}
            header="Common Mentions"
        />
    </Col>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKUnigrams(k, false, false, true);
            }}
            header="Common Hashtags"
        />
    </Col>
</Row>
<Row>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKNGrams(2, k);
            }}
            header="Common Bigrams"
        />
    </Col>
</Row>
<Row>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKNGrams(3, k);
            }}
            header="Common Trigrams"
        />
    </Col>
</Row>
<Row>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKNGrams(4, k);
            }}
            header="Common Fourgrams"
        />
    </Col>
</Row>
