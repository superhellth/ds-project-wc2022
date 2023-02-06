<script lang="ts">
    import { flip } from "svelte/animate";
    import { onMount } from "svelte";
    import { fly, fade, slide } from "svelte/transition";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let numTweets: number = 5025511;
    let numDays: number = 14;
    let visible: boolean = false;

    onMount(async () => {
        visible = true;
    });
</script>

<!-- <h1>Exploring the perception of the 2022 FIFA World Cup</h1> -->
{#if visible}
    <div in:fly={{ y: 200, duration: 2000 }} out:fade>
        <img src="Qatar-2022-1536x798.png" class="banner" />
    </div>
    <div style="display: flex; justify-content: center" in:fly={{ y: 200, duration: 2000, delay: 0 }} out:fade>
        <p>
            We collected <span class="highlight">{numTweets}</span> Tweets from
            <span class="highlight">12323</span>
            different users over the course of
            <span class="highlight">{numDays}</span> days.
        </p>
    </div>
{/if}

<style>
    p {
        font-size: 1.2em;
    }
    .banner {
        width: 100%;
        height: 300px;
        object-fit: scale-down;
        margin-top: 3em;
        margin-bottom: 3em;
    }
    .highlight {
        font-size: 2em;
        background-color: #6c1d45;
        color: white;
    }
</style>
