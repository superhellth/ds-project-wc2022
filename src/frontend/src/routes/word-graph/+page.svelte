<script lang="ts">
    import { onMount } from "svelte";
    import Sigma from "sigma";
    import Graph from "graphology";
    import {
        Accordion,
        AccordionItem,
        Breadcrumb,
        BreadcrumbItem,
        Button,
        Form,
        FormGroup,
        Icon,
        Input,
        Label,
        Modal,
    } from "sveltestrap";
    import type {
        Coordinates,
        EdgeDisplayData,
        NodeDisplayData,
    } from "sigma/types.js";
    import Loading from "src/svelte-components/Loading.svelte";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";

    let provider = MiddlewareProvider.getInstance();

    let renderer: Sigma;
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 1;
    let displayEdgelessNodes: boolean = true;
    let clusters: Map<string, Set<string>> = new Map<string, Set<string>>();
    let windowSize: number = 4;
    let windowSizeOptions: number[] = [2, 3, 4];
    let numEdges: number = 100000;
    let numEdgesOptions: number[] = [10000, 25000, 50000, 100000, 200000];
    let includeStopWords: boolean = false;
    let minNodeLength: number = 2;
    let minNodeLengthOptions: number[] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    let embeddingSize: number = 128;
    let embeddingSizeOptions: number[] = [-1, 1, 10, 128, 200, 300];
    let clusterAlg: string = "aggomerative";
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
    let nesOnly: boolean = false;

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
    let searchInput: any;
    let searchSuggestions: any;

    // Actions:
    function setSearchQuery(query: string) {
        state.searchQuery = query;

        if (searchInput.value !== query) searchInput.value = query;

        if (query) {
            const lcQuery = query.toLowerCase();
            const suggestions = displayGraph
                .nodes()
                .map((n) => ({
                    id: n,
                    label: displayGraph.getNodeAttribute(n, "label") as string,
                }))
                .filter(({ label }) => label.toLowerCase().includes(lcQuery));

            // If we have a single perfect match, them we remove the suggestions, and
            // we consider the user has selected a node through the datalist
            // autocomplete:
            if (suggestions.length === 1 && suggestions[0].label === query) {
                state.selectedNode = suggestions[0].id;
                state.suggestions = undefined;

                // Move the camera to center it on the selected node:
                const nodePosition = renderer.getNodeDisplayData(
                    state.selectedNode
                ) as Coordinates;
                renderer.getCamera().animate(nodePosition, {
                    duration: 500,
                });
            }
            // Else, we display the suggestions list:
            else {
                state.selectedNode = undefined;
                state.suggestions = new Set(suggestions.map(({ id }) => id));
            }
        }
        // If the query is empty, then we reset the selectedNode / suggestions state:
        else {
            state.selectedNode = undefined;
            state.suggestions = undefined;
        }

        // Refresh rendering:
        renderer.refresh();
    }

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

    onMount(async () => {
        const text = await provider.getWordGraph(
            4,
            100000,
            false,
            2,
            128,
            "agglomerative",
            12,
            nesOnly
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

        searchInput = document.getElementById(
            "search-input"
        ) as HTMLInputElement;
        searchSuggestions = document.getElementById(
            "suggestions"
        ) as HTMLDataListElement;
        searchSuggestions.innerHTML = displayGraph
            .nodes()
            .map(
                (node) =>
                    `<option value="${displayGraph.getNodeAttribute(
                        node,
                        "label"
                    )}"></option>`
            )
            .join("\n");
        searchInput.addEventListener("input", () => {
            setSearchQuery(searchInput.value || "");
        });
        searchInput.addEventListener("blur", () => {
            setSearchQuery("");
        });
    });

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
            nClusters,
            nesOnly
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
    <h1>Word Graph</h1>
    <Button
        type="button"
        style="background: rgba(0,0,0,0); color: var(--text-color); border: 0px"
        on:click={() => (controlsAreOpen = !controlsAreOpen)}
        ><Icon name="gear" /> Settings</Button
    >
</div>
<Breadcrumb style="float: clear">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Word Graph</BreadcrumbItem>
</Breadcrumb>
<div id="search" style="position: absolute; top: 8em; right: 30em; z-index: 1">
    <input
    style="width: 15em"
        type="search"
        id="search-input"
        list="suggestions"
        placeholder="Try searching for a node..."
    />
    <datalist id="suggestions" />
</div>
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
<h2>Results</h2>
<p>These results are suprisingly good, considering the only thing we input was the collocation counts. We have played around a bit with the parameters
    and found that this combination which is set as standard works best. We interpreted the topics the following way:
</p>
<ul>
    <li><h4 style="color: #FF0000">The Center Cluster</h4>
        <p>This cluster probably is the least meaningful one. It's made up of the most frequent words of the corpus. This topic includes: The Argentina
            vs Saudi Arabia match, the opening ceremony and generally all match announcements.
        </p>
    </li>
    <li><h4 style="color: #000000">#Cluster</h4>
        <p>Here we find a cluster consisting mainly of the hashtags used. It is obvious that such a cluster exists, since most people put all Hashtags
            they use at the end of their Tweet and thus most hashtags frequently appear together. Not too much information can be won from this cluster.
        </p>
    </li>
    <li><h4 style="color: #0008FF">#SayTheirNames</h4>
        <p>The first real topic! This clusters clearly represents the Iran Conflict discussion. We found that this cluster exists, even if we reduce the 
            number of clusters to find. So we can assume it is a much discussed and clearly outlined topic. 
        </p>
    </li>
    <li><h4 style="color: #004A08">C'mon England!</h4>
        <p>It's coming home... or maybe not... Like we've seen in the statistics about our data, there are many Tweets from England and thus it was to
            be expected, that the English football team would be quite a topic. It seems like people or news pages love to talk about english players.
        </p>
    </li>
    <li><h4 style="color: #00FFED">???</h4>
        <p>This cluster is hard to classify, we might need to do some more digging on that...
        </p>
    </li>
    <li><h4 style="color: #FF00C9">Steve Harvey</h4>
        <p>We call this one the "USA"-Cluster. It appears to be the cluster of topics american accounts tweeted about that are not related to the world
            cup. Things like Wrestling, Formula 1, Kanye West and... well Steve Harvey. Though we already know the Tweets about Steve Harvey mainly come
            from one single account, so it's not really a topic many people talk about but simply the result of spam.
        </p>
    </li>
    <li><h4 style="color: #FF8000">SUIIII!!!</h4>
        <p>Yep. There is a SUII-Cluster. But it's not, as you might suspect the result of Ronaldo fans tweeting about him, but the again the result of a
            few spam accounts pushing their product. This cluster most likely does not exist because there are so many tweets belonging to it, but because
            its very unrelated to other things people talked about.
        </p>
    </li>
    <li><h4 style="color: #F3FF00">NFT and Crypto</h4>
        <p>This cluster is quite similar to the one above. It's a spam cluster about NFTs and Cryptos. It's less specific but just as meaningless.
        </p>
    </li>
    <li><h4 style="color: #BF00FF">你好中国人！</h4>
        <p>Although we specified in our Twitter API Query, that we only want to collect english Tweets, we got Tweets with chinese and arabic hashtags.
            At least the chinese hashtags making up this cluster indicate that these Tweets are also scam related.
        </p>
    </li>
    <li><h4 style="color: #00FF01">Cluster 10</h4>
        <p>Another unclassifiable cluster, covering different unrelated topics like Harry and Meghan, some Leak controversy and the GOAT debate.
        </p>
    </li>
    <li><h4 style="color: #808080">Stand with Ukraine</h4>
        <p>This clusters is made up of Tweets about the war in Ukraine. It's the most isolated cluster.
        </p>
    </li>
</ul>
<Modal
    isOpen={controlsAreOpen}
    toggle={() => (controlsAreOpen = !controlsAreOpen)}
>
    <div id="graph-chooser" style="margin: 2em">
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
                <Label for="n-clusters-select"># of clusters</Label>
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
</Modal>

<style lang="scss">
    #sigma-container {
        width: 100%;
        height: 41em;
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
