<script lang="ts">
    import BasicCard from "src/svelte-components/BasicCard.svelte";
    import CountTableCard from "src/svelte-components/CountTableCard.svelte";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {
        Breadcrumb,
        BreadcrumbItem,
        Carousel,
        CarouselCaption,
        CarouselControl,
        CarouselIndicators,
        CarouselItem,
        Col,
        Row,
    } from "sveltestrap";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();
    const items = [
        "../wordcloud_unigrams_filtered.png",
        "../wordcloud_bigrams_filtered.png",
        "../wordcloud_trigrams_filtered.png",
        "../wordcloud_fourgrams_filtered.png",
    ];
    const subtexts = [
        "Unigram Wordcloud",
        "Bigram Wordcloud",
        "Trigram Wordcloud",
        "Fourgram Wordcloud",
    ];
    let activeIndex = 0;
</script>

<title>Statistics - Hashtags and Mentions</title>
<h1>Unigrams</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Unigrams</BreadcrumbItem>
</Breadcrumb>
<h4>Welcome to the unigram page!</h4>
<p>
    Here you can take a look at all the unigram counts we generated. These have
    been generated using the whole corpus. Without further processing these
    counts don't convey too much information, but still, there are some
    interesting things to notice here.
</p>
<p>
    Note: The unigram counts may take a while to load, if they are not loaded on
    middleware startup.
</p>

<Row>
    <Col>
        <BasicCard
            header="Word Clouds"
            footer="A word cloud is a visualization technique used to represent text
        data, where the size of each word corresponds to its frequency
        or importance within the text. The words are typically arranged
        in a random or clustered pattern, with the most frequent or
        important words displayed in a larger font size and bold color.
        The displayed wordclouds have been generated using unigrams,
        bigrams, trigrams and fourgrams. It is not hard to see that
        Quatar and the World Cup are the dominant themes in all sets and
        that they become even more dominant by increasing the n.
        Furthermore the graphics point out that the game 'Argentinia vs.
        Saudi Arabia' is really prominent in the dataset. Increasing the
        n also leads to focusing on a smaller set of topics e.g.
        'Ronaldo' disappears. While generating the wordclouds it was our
        strong focus to exclude unwanted tokens from evaluation, e.g.
        stopwords or non-ascii words and emojis, in order to to enhance
        the informative value of the graphs so that they provide a
        better insight into the most important topics."
        >
            <div slot="body">
                <Carousel {items} bind:activeIndex>
                    <CarouselIndicators bind:activeIndex {items} />
                    <div
                        class="carousel-inner"
                        style="margin: 20px; text-align: center"
                    >
                        {#each items as item, index}
                            <CarouselItem bind:activeIndex itemIndex={index}>
                                <img
                                    src={item}
                                    class="center"
                                    alt={`${item} ${index + 1}`}
                                />
                                <CarouselCaption
                                    captionHeader={subtexts[index]}
                                    captionText=""
                                />
                            </CarouselItem>
                        {/each}
                    </div>
                    <CarouselControl
                        direction="prev"
                        bind:activeIndex
                        {items}
                    />
                    <CarouselControl
                        direction="next"
                        bind:activeIndex
                        {items}
                    />
                </Carousel>
            </div>
        </BasicCard>
    </Col>
</Row>

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
    <Col>
        <CountTableCard
            providingFunction={(k, includeStop) => {
                return provider.getTopKUnigrams(k, false, true, false);
            }}
            header="Common Mentions"
            footer="This already gives us an idea which teams were talked about a lot and which other topics apart from the tournament have found their way into our corpus. As seen on the Home page of this Website most Tweets are from the UK and US, this also explains why the most frequently mentioned football teams are the one of the US '@usmnt' and the one of England '@england'. Furthermore the three BTS mentions '@bts_twt', '@bighit_music' and '@bts_bighit' confirm the assumption from above that the opening ceremony was a well discussed topic. The mentions unrelated to the tournament like '@iamsteveharvey' and '@suinsdapp' emphasize that there are quite some spam Tweets in our Dataset."
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

<style lang="scss">
    .center {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 70%;
    }
</style>
