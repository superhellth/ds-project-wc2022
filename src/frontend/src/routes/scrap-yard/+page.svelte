<script lang="ts">
    // Import Svelte components used in this script
    import {
        Alert,
        Breadcrumb,
        BreadcrumbItem,
    } from "sveltestrap";
    import {fly} from "svelte/transition";
</script>

<title>Experimental - Scrap Yard</title>
<h1>Tweet Query</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Scrap Yard</BreadcrumbItem>
</Breadcrumb>

<div in:fly={{ x: 400, duration: 400, delay: 200 }}>
    <h4>NMF</h4>
    <p>
        NMF (Non-negative Matrix Factorization) is a technique widely used in topic modeling that originates from
        Linear Algebra. The goal of this algorithm is to extract the underlying topics of a dataset. It operates only
        on the Document-Term-Matrix, where each tweet is considered as an individual document, performing
        transformations. NMF decomposes the Document-Term-Matrix into a Document-Topic matrix and a Topic-Term matrix.
    </p>
    <Alert color="primary">
        'listened pisses equal enter murders method partido burger'
    </Alert>
    <Alert color="secondary">
        'andros verified pk dinamarca wallahi fit womenlifefreedom losers'
    </Alert>
    <Alert color="success">
        'cultural massacred android stones ferdinand mistake truth annoyed'
    </Alert>
    <Alert color="danger">
        'economy pe sexuality nftcollector luuk thigh tribes gift'
    </Alert>
    <Alert color="warning">
        'investment executive fast clue palace arabs 20 atrocities'
    </Alert>
    <Alert color="info">
        'labour thfc bio lifetime ferdinand luuk goalie fake'
    </Alert>
    <Alert color="light">
        'englandsquad sexuality pe bio thigh enter worldcupticket fucking'
    </Alert>
    <Alert color="dark">
        'dumfries emir fishing mar reality abudhabigp lifts pot'
    </Alert>
    <p>
        It is easy to see that NMF does not provide easy-to-read topics in our application. This could be the case
        for several reasons. First of all, it is likely a consequence of training NMF on 1,000,000 Tweets, which
        includes a wide range of topics where many of them are not relevant, such as spam posts. Furthermore, NMF is a
        relatively simple algorithm compared to more sophisticated transformer-based models. Finally, we did not make a
        selection on the tweets, so it is likely that the amount of noise in the training dataset is high, which would
        definitely worsen the results.
    </p>
    <h4>SVD</h4>
    <p>
        SVD (Singular Value Decomposition) is a technique widely used in topic modeling that originates from Linear
        Algebra.
        The goal of this algorithm is to extract the underlying topics of a dataset. It operates only on the
        Document-Term-Matrix, where each tweet is considered as an individual document, performing transformations.
        After training on our whole dataset in order to extract the eight most prominent topics described by fifteen
        words, it provides the following information:
    </p>
    <Alert color="primary">
        'link live world cup vs fifaworldcup 2022 qatar2022 fifa qatar stream argentina worldcup2022
            fifaworldcup2022 qatarworldcup2022'
    </Alert>
    <Alert color="secondary">
        'world cup qatar 2022 fifa nt win football team messi game opening time final england'
    </Alert>
    <Alert color="success">
        'live vs 2022 fifa stream cup world qatar2022 hd ceremony opening streaming ecuador watch retweet'
    </Alert>
    <Alert color="danger">
        'fifaworldcup qatar2022 qatar argentina vs nt messi england game football worldcup2022 qatarworldcup2022
            team match iran'
    </Alert>
    <Alert color="warning">
        'qatar 2022 fifa ecuador opening ceremony worldcup senegal link fifaworldcup2022 worldcup2022 doha host
            rights massage'
    </Alert>
    <Alert color="info">
        'vs argentina nt qatar messi brazil england game netherlands croatia win mexico saudi team arabia'
    </Alert>
    <Alert color="light">
        'argentina messi fifa 2022 saudi mexico arabia lionel ceremony opening goat argentinavsmexico saudiarabia
            fifaworldcup2022 ronaldo'
    </Alert>
    <Alert color="dark">
        'vs brazil england croatia argentina 2022 usa fifa netherlands worldcup2022 qatar2022 japan iran france
            wales'
    </Alert>
    <p>
        It is easy to see that the most important topics according to SVD are all strongly related to the World Cup
        with a focus on football. Furthermore, many countries are highly prominent, such as Argentina and Saudi Arabia,
        and some hashtags like #FIFAWORLDCUP2022. Additionally, Messi is highly important since both "Messi" and
        "Lionel" appear.
        <br>
        However, the output provided is not the best result because it lacks context and specificity. The topics
        generated are too broad and generic, making it difficult to gain any insights or draw meaningful conclusions
        from them. This is probably a result of training SVD on the whole dataset without further.cleaning and
        preparation. This results in the appearance of words that are highly associated with spam tweets in our dataset,
        such as "streaming" and "live."
        <br>
        Additionally, it is worth noting that we used truncated SVD, a less precise deviation from the original
        algorithm that has better performance but may have worsened our results. This was necessary since our dataset is
        very extensive.
        <br>
        In conclusion, the SVD did not provide many useful insights on the topics discussed in our dataset. However, it
        is an important example of the dependency on cleaned and optimized input data for an algorithm to provide useful
        results. To improve the quality of the output, it is essential to conduct further cleaning and preparation of
        the dataset and consider using more sophisticated algorithms, such as transformer-based models, for topic
        modeling.
    </p>
</div>
