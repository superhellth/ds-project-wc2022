<script lang="ts">
    import CountTableCard from "src/svelte-components/CountTableCard.svelte";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import { Breadcrumb, BreadcrumbItem, Col, Row } from "sveltestrap";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();
</script>

<title>Statistics - Hashtags and Mentions</title>
<h1>N-grams</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>n-grams</BreadcrumbItem>
</Breadcrumb>
<h4>Welcome to the n-gram page!</h4>
<p>Here you can take a look at all the n-gram counts we generated. These have been generated using the whole corpus.
    Without further processing these counts don't convey too much information, but still, there are some interesting things to notice here.</p>
<p>Note: The n-gram counts make take a while to load, if they are not loaded on middleware startup.</p>

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
            footer="These tokens are very generic and many of these are simple emojis or single characters. But if you take a look at number 72 ('opening') and number 99 ('jungkook', lead artist of BTS, the band who played at the opening ceremony) without stop words, you can see that quite a good part of the Tweets we collected are about the opening. This gives us a first impression about what topics may have been talked about. However the opening might also be slightly overrepresented since we lack Tweets from later in the tournament while having collected all the Tweets from the days before and after the opening."
            keyColumnName="Token"
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
            footer="Now this already gives us an idea which teams were talked about a lot and which other topics apart from the tournament have found their way into our corpus. As seen on the Home page of this Website most Tweets are from the UK and US, this also explains why the most frequently mentioned football teams are the one of the US '@usmnt' and the one of England '@england'. Furthermore the three BTS mentions '@bts_twt', '@bighit_music' and '@bts_bighit' confirm the assumption from above that the opening ceremony was a well discussed topic. The mentions unrelated to the tournament like '@iamsteveharvey' and '@suinsdapp' emphasize that there are quite some spam Tweets in our Dataset."
            keyColumnName="Mention"
        />
    </Col>
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKUnigrams(k, false, false, true);
            }}
            header="Common Hashtags"
            footer="Now this is an interesting one. These hashtags reflected what we already found out from the unigrams and the mentions, but it also shows one new thing. Namely the presence of the Iran Conflict in our Dataset. The hashtags #saytheirnames and #mahsaamini clearly indicate that. The reason this is interesting is, that this is a politic topic mostly unrelated to the tournament only connected by the Iran taking part in the world cup and the gesture they made before their match against Wales. This means the political situation in the Iran is more interesting to people than the political situation in Qatar. A first indicator to the answer to the question whether or not the Sportswashing of Qatar was successful."
            keyColumnName="Hashtag"
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
            keyColumnName="Bigram"
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
            keyColumnName="Trigram"
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
            keyColumnName="Fourgram"
        />
    </Col>
</Row>
