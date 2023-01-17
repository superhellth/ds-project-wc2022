<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    
    onMount(async () => {
        
        const res = await fetch('collocations3.gexf');
        const text = await res.text();

        const Graph = await import("graphology").then(m => m.default)
        const { parse } = await import('graphology-gexf/browser');
        const graph = parse(Graph, text);

        // Retrieve some useful DOM elements:
        const container = document.getElementById("sigma-container") as HTMLElement;

        // Instanciate sigma:
        const renderer = new Sigma(graph, container, {
        minCameraRatio: 0.1,
        maxCameraRatio: 10,
        });
    })

    
</script>

<div id="sigma-container"></div>

<style>
    #sigma-container {
        width: 100%;
        height: 50em;
        margin: 0;
        padding: 0;
        overflow: hidden;
      }
</style>