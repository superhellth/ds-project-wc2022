<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    import Graph from "graphology";
    import { Input } from "sveltestrap";
    import type { EdgeDisplayData } from "sigma/types.js";

    let renderer: Sigma;
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 1;

    interface State {
        hoveredNode?: string;
        searchQuery: string;

        // State derived from query:
        selectedNode?: string;
        suggestions?: Set<string>;

        // State derived from hovered node:
        hoveredNeighbors?: Set<string>;
    }
    const state: State = { searchQuery: "" };

    onMount(async () => {
        const res = await fetch("word-graph.gexf");
        const text = await res.text();

        const Graph = await import("graphology").then((m) => m.default);
        const { parse } = await import("graphology-gexf/browser");
        displayGraph = parse(Graph, text);

        displayGraph.forEachNode(
            (node, attributes) => (attributes.size = Math.min(attributes.degree * 0.1, 3.5))
        );
        displayGraph.forEachEdge(
            (node, attributes) => (attributes.size = 0.001)
        );

        originalGraph.import(displayGraph);

        const container = document.getElementById(
            "sigma-container"
        ) as HTMLElement;

        renderer = new Sigma(displayGraph, container, {
            minCameraRatio: 0.001,
            maxCameraRatio: 10,
        });

        renderer.on("enterNode", ({ node }) => {
            setHoveredNode(node);
        });
        renderer.on("leaveNode", () => {
            setHoveredNode(undefined);
        });

        renderer.setSetting("nodeReducer", (node, data) => {
            const res: Partial<NodeDisplayData> = { ...data };

            if (
                state.hoveredNeighbors &&
                !state.hoveredNeighbors.has(node) &&
                state.hoveredNode !== node
            ) {
                res.label = "";
                res.color = "#f6f6f6";
            }

            if (state.selectedNode === node) {
                res.highlighted = true;
            } else if (state.suggestions && !state.suggestions.has(node)) {
                res.label = "";
                res.color = "#f6f6f6";
            }

            return res;
        });

        // Render edges accordingly to the internal state:
        // 1. If a node is hovered, the edge is hidden if it is not connected to the
        //    node
        // 2. If there is a query, the edge is only visible if it connects two
        //    suggestions
        renderer.setSetting("edgeReducer", (edge, data) => {
            const res: Partial<EdgeDisplayData> = { ...data };

            if (
                state.hoveredNode &&
                !displayGraph.hasExtremity(edge, state.hoveredNode)
            ) {
                res.hidden = true;
            }

            if (
                state.suggestions &&
                (!state.suggestions.has(displayGraph.source(edge)) ||
                    !state.suggestions.has(displayGraph.target(edge)))
            ) {
                res.hidden = true;
            }

            return res;
        });
    });

    function setHoveredNode(node?: string) {
        if (node) {
            state.hoveredNode = node;
            state.hoveredNeighbors = new Set(displayGraph.neighbors(node));
        } else {
            state.hoveredNode = undefined;
            state.hoveredNeighbors = undefined;
        }

        // Refresh rendering:
        renderer.refresh();
    }

    async function changeEdgeThreshold(threshold: number) {
        if (displayGraph == null) {
            return;
        }

        let edgesByWeights: Map<string, number> = new Map<string, number>();

        displayGraph.forEachEdge((edge) => displayGraph.dropEdge(edge));
        displayGraph.forEachNode((node) => displayGraph.dropNode(node));
        displayGraph.import(originalGraph.export());

        displayGraph.forEachEdge((edge, attributes) => {
            edgesByWeights.set(edge, attributes.weight);
        });
        let sortedEdges: [string, number][] = [
            ...edgesByWeights.entries(),
        ].sort((a, b) => b[1] - a[1]);
        let numEdges = sortedEdges.length;
        sortedEdges = sortedEdges.slice(0, Math.round(threshold * numEdges));
        let edgesToKeep: Set<string> = new Set();
        for (var i = 0; i < sortedEdges.length; i++) {
            edgesToKeep.add(sortedEdges[i][0]);
        }

        let edgesToRemove: Set<string> = new Set();
        displayGraph.forEachEdge((edge) => {
            if (!edgesToKeep.has(edge)) {
                edgesToRemove.add(edge);
            }
        });
        console.log(edgesToRemove);

        edgesToRemove.forEach((edge) => displayGraph.dropEdge(edge));
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
<div id="sigma-container" />

<style>
    #sigma-container {
        width: 100%;
        height: 50em;
        margin: 0;
        padding: 0;
        overflow: hidden;
    }
</style>
