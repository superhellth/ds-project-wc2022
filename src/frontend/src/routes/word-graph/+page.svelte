<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    import Graph from "graphology";
    import {
        Accordion,
        AccordionItem,
        Button,
        Form,
        FormGroup,
        Input,
        Label,
        Offcanvas,
    } from "sveltestrap";
    import type { EdgeDisplayData } from "sigma/types.js";
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";

    let provider = ElasticProvider.getInstance();

    let renderer: Sigma;
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 1;
    let displayEdgelessNodes: boolean = true;
    let clusters: Map<string, Set<string>> = new Map<string, Set<string>>();
    let windowSize: number = 4;
    let windowSizeOptions: number[] = [2, 3, 4];
    let numEdges: number = 50000;
    let numEdgesOptions: number[] = [10000, 25000, 50000, 100000, 200000];
    let includeStopWords: boolean = false;
    let minNodeLength: number = 2;
    let minNodeLengthOptions: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let embeddingSize: number = 128;
    let embeddingSizeOptions: number[] = [-1, 1, 10, 128, 200, 300];
    let clusterAlg: string = "k-means";
    let clusterAlgOptions: string[] = [
        "spectral",
        "k-means",
        "agglomerative",
        "mean-shift",
        "affinity-propagation",
        "dbscan",
        "optics",
        "birch",
        "mini-batch-k-means",
    ];
    let nClusters: number = 11;
    let nClustersOptions: number[] = [
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
    ];
    let loading: boolean = false;
    let controlsAreOpen: boolean = false;

    // Code taken from https://codesandbox.io/s/github/jacomyal/sigma.js/tree/main/examples/use-reducers
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
        const text = await provider.getWordGraph(
            4,
            50000,
            false,
            2,
            128,
            "k-means",
            11
        );

        const Graph = await import("graphology").then((m) => m.default);
        const { parse } = await import("graphology-gexf/browser");
        displayGraph = parse(Graph, text);

        displayGraph.forEachNode((node, attributes) => {
            attributes.size = Math.min(attributes.degree * 0.1, 3.5);
            if (clusters.get(attributes.color) == undefined) {
                clusters.set(attributes.color, new Set<string>([node]));
            } else {
                clusters.get(attributes.color)?.add(node);
            }
        });
        clusters = clusters;
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
        edgesToRemove.forEach((edge) => displayGraph.dropEdge(edge));

        if (!displayEdgelessNodes) {
            let toRemove: Set<string> = new Set();
            displayGraph.forEachNode((node) => {
                if (displayGraph.edges(node).length == 0) {
                    toRemove.add(node);
                }
            });
            toRemove.forEach((node) => displayGraph.dropNode(node));
        }
    }

    async function toggleEdgelessNodes(displayEdgelessNodes: boolean) {
        if (!displayEdgelessNodes) {
            let toRemove: Set<string> = new Set();
            displayGraph.forEachNode((node) => {
                if (displayGraph.edges(node).length == 0) {
                    toRemove.add(node);
                }
            });
            toRemove.forEach((node) => displayGraph.dropNode(node));
        }
    }

    async function rebuildGraph() {
        loading = true;
        const text = await provider.getWordGraph(
            windowSize,
            numEdges,
            includeStopWords,
            minNodeLength,
            embeddingSize,
            clusterAlg,
            nClusters
        );

        const Graph = await import("graphology").then((m) => m.default);
        const { parse } = await import("graphology-gexf/browser");
        let newGraph = parse(Graph, text);

        displayGraph.forEachEdge((edge) => displayGraph.dropEdge(edge));
        displayGraph.forEachNode((node) => displayGraph.dropNode(node));
        clusters = new Map<string, Set<string>>();
        displayGraph.import(newGraph.export());

        displayGraph.forEachNode((node, attributes) => {
            attributes.size = Math.min(attributes.degree * 0.1, 3.5);
            if (clusters.get(attributes.color) == undefined) {
                clusters.set(attributes.color, new Set<string>([node]));
            } else {
                clusters.get(attributes.color)?.add(node);
            }
        });
        clusters = clusters;
        displayGraph.forEachEdge(
            (node, attributes) => (attributes.size = 0.001)
        );

        originalGraph = new Graph();
        originalGraph = parse(Graph, text);
        displayGraph = displayGraph;
        loading = false;
        controlsAreOpen = false;
    }

    $: changeEdgeThreshold(threshold);
    $: toggleEdgelessNodes(displayEdgelessNodes);
</script>

<title>Text Analytics - Word Graph</title>

<div style="display: flex; justify-content: space-between">
    <h2>Word Graph</h2>
    <Button
        type="button"
        on:click={() => controlsAreOpen = !controlsAreOpen}
        style="float: right;">Graph settings</Button
    >
</div>
<div style="height: 1px; background: black; margin-top: 2px" />
<div id="graph-container">
    <div id="sigma-container" />
    <div id="cluster-div">
        <Form>
            <FormGroup>
                <legend>Top Words by Cluster</legend>
                <Accordion id="clusters">
                    {#each Array.from(clusters.keys()) as cluster, i}
                        <AccordionItem header={"Cluster " + (i + 1)}>
                            <ul>
                                {#each Array.from(clusters.get(cluster))
                                    .sort((nodeA, nodeB) => originalGraph.getNodeAttributes(nodeA).weight - originalGraph.getNodeAttributes(nodeB).weight)
                                    .slice(0, 10) as token}
                                    <li style="color: {cluster}">{token}</li>
                                {/each}
                            </ul>
                        </AccordionItem>
                    {:else}
                        <Loading displayString="Cluster" />
                    {/each}
                </Accordion>
            </FormGroup>
        </Form>
    </div>
</div>
<Form>
    <FormGroup>
        <Label for="edgeThreshold">% of Edges to display</Label>
        <Input
            type="range"
            name="range"
            id="edgeThreshold"
            min={0}
            max={1}
            step={0.01}
            bind:value={threshold}
        />
        <Input
            id="edgelessNodes"
            type="checkbox"
            label="Display Nodes without Edges"
            bind:checked={displayEdgelessNodes}
        />
    </FormGroup>
</Form>
<Offcanvas isOpen={controlsAreOpen} toggle={() => controlsAreOpen = !controlsAreOpen} placement="end">
    <div id="graph-chooser">
        <Form>
            <legend>Filtering</legend>
            <FormGroup>
                <Label for="window-size-select">Window Size</Label>
                <Input
                    type="select"
                    name="select"
                    id="window-size-select"
                    bind:value={windowSize}
                >
                    {#each windowSizeOptions as windowSize}
                        <option>{windowSize}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup>
                <Label for="num-edges-select"
                    >Number of edges(collocations)</Label
                >
                <Input
                    type="select"
                    name="select"
                    id="num-edges-select"
                    bind:value={numEdges}
                >
                    {#each numEdgesOptions as numEdges_}
                        <option>{numEdges_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup>
                <Label for="min-node-length-select"
                    >Minimun number of characters in node</Label
                >
                <Input
                    type="select"
                    name="select"
                    id="min-node-length-select"
                    bind:value={minNodeLength}
                >
                    {#each minNodeLengthOptions as minNodeLength_}
                        <option>{minNodeLength_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup>
                <Label for="include-stop-select">Include stop word nodes</Label>
                <Input
                    id="r3"
                    type="radio"
                    bind:group={includeStopWords}
                    value={true}
                    label="Yes"
                />
                <Input
                    id="r4"
                    type="radio"
                    bind:group={includeStopWords}
                    value={false}
                    label="No"
                />
            </FormGroup>
        </Form>
        <Form>
            <legend>Clustering</legend>
            <FormGroup>
                <Label for="cluster-alg-select">Clustering Algorithm</Label>
                <Input
                    type="select"
                    name="select"
                    id="cluster-alg-select"
                    bind:value={clusterAlg}
                >
                    {#each clusterAlgOptions as clusterAlg_}
                        <option>{clusterAlg_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup>
                <Label for="n-clusters-select">Clustering Algorithm</Label>
                <Input
                    type="select"
                    name="select"
                    id="n-clusters-select"
                    bind:value={nClusters}
                >
                    {#each nClustersOptions as nClusters_}
                        <option>{nClusters_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup>
                <Label for="embedding-size-select"
                    >Size of Node2Vec embedding</Label
                >
                <Input
                    type="select"
                    name="select"
                    id="embedding-size-select"
                    bind:value={embeddingSize}
                >
                    {#each embeddingSizeOptions as embeddingSize_}
                        <option>{embeddingSize_}</option>
                    {/each}
                </Input>
            </FormGroup>
        </Form>
        <Button
            type="button"
            on:click={() => rebuildGraph()}
            style="background: blue">Rebuild Graph</Button
        >
        {#if loading}
                <Loading displayString="graph" />
        {/if}
    </div>
</Offcanvas>

<style>
    #sigma-container {
        width: 100%;
        height: 45em;
        margin: 0;
        padding: 0;
        overflow: hidden;
        margin-right: 2em;
    }
    #graph-container {
        display: flex;
        justify-content: space-around;
    }
    #cluster-div {
        min-width: 25em;
    }
</style>
