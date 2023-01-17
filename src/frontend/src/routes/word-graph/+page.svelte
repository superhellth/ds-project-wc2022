<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    import Graph from "graphology";
    import { Input } from "sveltestrap";
    
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 1;
    
    onMount(async () => {
        const res = await fetch('collocations2nostop.gexf');
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

        let edgesByWeights: Map<string, number> = new Map<string, number>;

        displayGraph.forEachEdge((edge) => displayGraph.dropEdge(edge));
        displayGraph.forEachNode((node) => displayGraph.dropNode(node));
        displayGraph.import(originalGraph.export());

        displayGraph.forEachEdge((edge, attributes) => {
            edgesByWeights.set(edge, attributes.weight);
        })
        let sortedEdges: [string, number][] = [...edgesByWeights.entries()].sort((a, b) => b[1] - a[1]);
        let numEdges = sortedEdges.length;
        sortedEdges = sortedEdges.slice(0, Math.round(threshold * numEdges))
        let edgesToKeep: Set<string> = new Set()
        for (var i = 0; i < sortedEdges.length; i++) {
            edgesToKeep.add(sortedEdges[i][0])
        }

        let edgesToRemove: Set<string> = new Set();
        displayGraph.forEachEdge((edge) => {
            if (!edgesToKeep.has(edge)) {
                edgesToRemove.add(edge)
            }
        });
        console.log(edgesToRemove)
        
        edgesToRemove.forEach((edge) => displayGraph.dropEdge(edge))
    }

    $: changeEdgeThreshold(threshold);
    
</script>

<Input
      type="range"
      name="range"
      id="exampleRange"
      min={0}
      max={1}
      step={0.01}
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