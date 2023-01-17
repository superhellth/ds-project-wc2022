<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    import Graph from "graphology";
    import { Input } from "sveltestrap";
    
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 0;
    
    onMount(async () => {
        const res = await fetch('collocations3.gexf');
        const text = await res.text();

        const Graph = await import("graphology").then(m => m.default)
        const { parse } = await import('graphology-gexf/browser');
        displayGraph = parse(Graph, text);
        originalGraph.import(displayGraph)

        const container = document.getElementById("sigma-container") as HTMLElement;

        const renderer = new Sigma(displayGraph, container, {
            minCameraRatio: 0.01,
            maxCameraRatio: 10,
        });
    })

    async function changeEdgeThreshold(threshold: number) {
        if (displayGraph == null) {
            return;
        }

        let maxWeight = -1

        displayGraph.forEachEdge((edge) => displayGraph.dropEdge(edge))
        displayGraph.forEachNode((node) => displayGraph.dropNode(node))
        displayGraph.import(originalGraph.export())

        displayGraph.forEachEdge((edge, attributes) => {
            if (attributes.weight > maxWeight) {
                maxWeight = attributes.weight;
            }
        })

        let edgesToRemove = displayGraph.filterEdges((edge, attributes) => attributes.weight > maxWeight * threshold)
        console.log(edgesToRemove.length)
        
        for (let edge in edgesToRemove) {
            displayGraph.dropEdge(edge);
        }
    }

    $: changeEdgeThreshold(threshold);
    
</script>

<Input
      type="range"
      name="range"
      id="exampleRange"
      min={0}
      max={0.01}
      step={0.000001}
      bind:value={threshold}
    />
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