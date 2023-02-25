<script lang="ts">
    // Import Svelte components used in this script
    import {
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
        This did not work because...
    </p>
    <h4>SVD</h4>
    <p>
        SVD (Singular Value Decomposition) originates from Linear Algebra and is a technique widely used in topic modeling. The goal of this algorithm is extracting the underlying topics of our dataset
        It is one of the less sophisticated methods since it is operating onyl the Document-Term-Matrix, where each tweet is considered as an individual document, performing transformations.
        After it has been trained on our whole dataset in order to extract the eigth most prominent topics discribed by fifteen words it provides the following information:

        <li>'link live world cup vs fifaworldcup 2022 qatar2022 fifa qatar stream argentina worldcup2022 fifaworldcup2022 qatarworldcup2022'</li>
        <li>'world cup qatar 2022 fifa nt win football team messi game opening time final england'</li>
        <li>'live vs 2022 fifa stream cup world qatar2022 hd ceremony opening streaming ecuador watch retweet'</li>
        <li>'fifaworldcup qatar2022 qatar argentina vs nt messi england game football worldcup2022 qatarworldcup2022 team match iran'</li>
        <li>'qatar 2022 fifa ecuador opening ceremony worldcup senegal link fifaworldcup2022 worldcup2022 doha host rights massage'</li>
        <li>'vs argentina nt qatar messi brazil england game netherlands croatia win mexico saudi team arabia'</li>
        <li>'argentina messi fifa 2022 saudi mexico arabia lionel ceremony opening goat argentinavsmexico saudiarabia fifaworldcup2022 ronaldo'</li>
        <li>'vs brazil england croatia argentina 2022 usa fifa netherlands worldcup2022 qatar2022 japan iran france wales'</li>

        It is easy to see that the most important topics according to SVD are all strongly related to the World Championship with focus on the football itself.
        Furthermore there are many countries highly prominent e.g. Argentinia or Saui Arabia and some hashtags like #FIFAWORLDCUP2022. Additionally Messi is highly important since both Messi and Lionel appear.
        However, the output you provided is not the best result because it lacks context and specificity. The topics generated are too broad and generic, which makes it difficult to gain any insights or draw meaningful conclusions from them.
        This is probably a result of training the SVD on the whole dataset without further cleaning and preparation. This results for example in the appearance of words which are highly associated with spam tweets in our dataset e.g. streaming, live etc.
        Additionally it is to mention that we used the truncated SVD, a less precise deviation from the original algorithm which has a better performance. This was necessary since our dataset is very extensive. This probably worsens our results as well.
        In conclusion the SVD did not hold up much usefull isghts on the topics discussed in our dataset but is an important example for the dependency on cleaned and optimised input data for an algorithm in order to provide useful results.
    </p>
</div>
