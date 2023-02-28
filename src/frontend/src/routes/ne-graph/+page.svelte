<script lang="ts">
    import {onMount} from "svelte";
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
    import {fly} from "svelte/transition";

    let provider = MiddlewareProvider.getInstance();

    let renderer: Sigma;
    let displayGraph: Graph;
    let originalGraph: Graph = new Graph();
    let threshold: number = 1;
    let displayEdgelessNodes: boolean = true;
    let clusters: Map<string, Set<string>> = new Map<string, Set<string>>();
    let neTypeSelection: Map<string, boolean> = new Map<string, boolean>();
    neTypeSelection.set("DATE", true);
    neTypeSelection.set("PERSON", true);
    neTypeSelection.set("GPE", true);
    neTypeSelection.set("LOC", true);
    neTypeSelection.set("MONEY", true);
    neTypeSelection.set("TIME", true);
    neTypeSelection.set("PRODUCT", true);
    neTypeSelection.set("CARDINAL", true);
    neTypeSelection.set("ORDINAL", true);
    neTypeSelection.set("QUANTITY", true);
    neTypeSelection.set("EVENT", true);
    neTypeSelection.set("FAC", true);
    neTypeSelection.set("LANGUAGE", true);
    neTypeSelection.set("LAW", true);
    neTypeSelection.set("NORP", true);
    neTypeSelection.set("PERCENT", true);
    neTypeSelection.set("WORK_OF_ART", true);
    let selectedNeTypes: string[] = [];
    $: {
        selectedNeTypes = [];
        neTypeSelection.forEach((value, key) => {
            if (value) {
                selectedNeTypes.push(key);
            }
        });
    }
    let numEdges: number = 25000;
    let numEdgesOptions: number[] = [10000, 25000, 50000, 100000, 200000];
    let minNodeLength: number = 2;
    let embeddingSize: number = 128;
    let clusterAlg: string = "agglomerative";
    let nClusters: number = 12;
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

    const state: State = {searchQuery: ""};
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
                .filter(({label}) => label.toLowerCase().includes(lcQuery));

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
                state.suggestions = new Set(suggestions.map(({id}) => id));
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

    let visible: boolean = false;

    onMount(async () => {
        visible = true;
        const text = await provider.getWordGraph(
            0,
            numEdges,
            false,
            minNodeLength,
            embeddingSize,
            clusterAlg,
            nClusters,
            true
        );

        const Graph = await import("graphology").then((m) => m.default);
        const {parse} = await import("graphology-gexf/browser");
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
            "sigma-container2"
        ) as HTMLElement;

        renderer = new Sigma(displayGraph, container, {
            minCameraRatio: 0.001,
            maxCameraRatio: 10,
        });

        renderer.on("enterNode", ({node}) => {
            setHoveredNode(node);
        });
        renderer.on("leaveNode", () => {
            setHoveredNode(undefined);
        });

        renderer.setSetting("nodeReducer", (node, data) => {
            const res: Partial<NodeDisplayData> = {...data};

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
            const res: Partial<EdgeDisplayData> = {...data};

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
            "search2-input"
        ) as HTMLInputElement;
        searchSuggestions = document.getElementById(
            "suggestions2"
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
        filterTypeNodes();
    });

    function filterTypeNodes() {
        displayGraph.forEachEdge((edge) => displayGraph.dropEdge(edge));
        displayGraph.forEachNode((node) => displayGraph.dropNode(node));
        displayGraph.import(originalGraph.export());

        let nodesToRemove: Set<string> = new Set();
        displayGraph.forEachNode((node, attributes) => {
            let nodeType = node.split("&&")[1];
            console.log(nodeType);
            if (!selectedNeTypes.includes(nodeType)) {
                nodesToRemove.add(node);
            }
            attributes.label = node.split("&&")[0].replaceAll("_", " ");
        });
        console.log(selectedNeTypes);
        console.log(nodesToRemove);
        nodesToRemove.forEach((node) => displayGraph.dropNode(node));
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
            0,
            numEdges,
            false,
            minNodeLength,
            embeddingSize,
            clusterAlg,
            nClusters,
            true
        );

        const Graph = await import("graphology").then((m) => m.default);
        const {parse} = await import("graphology-gexf/browser");
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
        filterTypeNodes();
    }

    $: changeEdgeThreshold(threshold);
    $: toggleEdgelessNodes(displayEdgelessNodes);
</script>

<title>Text Analytics - Named Entities</title>

<div style="display: flex; justify-content: space-between">
    <h1>Named Entities</h1>
    <Button
            type="button"
            style="background: rgba(0,0,0,0); color: var(--text-color); border: 0px"
            on:click={() => (controlsAreOpen = !controlsAreOpen)}
    >
        <Icon name="gear"/>
        Settings
    </Button
    >
</div>
<Breadcrumb style="float: clear">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Named Entities</BreadcrumbItem>
</Breadcrumb>
{#if visible}
    <div
            id="search2"
            style="position: absolute; top: 8em; right: 30em; z-index: 1"
            in:fly={{ y: 400, duration: 1000, delay: 1400 }}
    >
        <input
                style="width: 15em"
                type="search"
                id="search2-input"
                list="suggestions"
                placeholder="Try searching for a node..."
        />
        <datalist id="suggestions2"/>
    </div>
{/if}
<div id="graph-container2">
    {#if visible}
        <div
                id="sigma-container2"
                in:fly={{ y: 400, duration: 1000, delay: 1000 }}
        />
        <div id="cluster-div2" in:fly={{ x: 400, duration: 1000, delay: 100 }}>
            <Form>
                <FormGroup>
                    <legend>Top Entities by Cluster</legend>
                    <Accordion id="clusters">
                        {#each Array.from(clusters.keys()) as cluster, i}
                            <AccordionItem header={"Cluster " + (i + 1)}>
                                <ul>
                                    {#each Array.from(clusters.get(cluster))
                                        .sort((nodeA, nodeB) => originalGraph.getNodeAttributes(nodeA).weight - originalGraph.getNodeAttributes(nodeB).weight)
                                        .slice(0, 10) as token}
                                        <li style="color: {cluster}">
                                            {token
                                                .split("&&")[0]
                                                .replaceAll("_", " ")}
                                        </li>
                                    {/each}
                                </ul>
                            </AccordionItem>
                        {:else}
                            <Loading displayString="Cluster"/>
                        {/each}
                    </Accordion>
                </FormGroup>
            </Form>
        </div>
    {/if}
</div>
{#if visible}
    <div in:fly={{ x: 400, duration: 1000, delay: 100 }}>
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
    </div>
{/if}
<h2>Results</h2>
<p>
    This graph conveys a little less information than the word graph does,
    however there are some interesting things to note here. The topics/clusters
    are quite similar to the clusters in the word graph.
</p>
<ul>
    <li>
        <h4 style="color: #F3FF00">Iran again</h4>
        <p>
            In this graph we also have an Iran cluster. It was to be expected,
            that the topics would be similar to the word graph topics, still it
            emphasizes the relevance of this topic in our corpus.
        </p>
    </li>
    <li>
        <h4 style="color: #004A08">Cricket</h4>
        <p>
            This cluster is new. It is mainly about the T20 Cricket world
            championship. Just another topic more relevant than critizism about
            Qatar.
        </p>
    </li>
    <li>
        <h4 style="color: #FF00C9">Israel and palastine</h4>
        <p>
            There seem to be a handful of noticeable things that happened that
            have to do with the conflict between Israel and Palastine. For
            example the Israelian Prime Minister publically celebrated the
            victory of Saudi Arabia over Argentina. Moreover there was an
            agreement from Qatar with Palastine and Israel to allow people from
            both nations to come to the world cup.
        </p>
    </li>
    <li>
        <h4 style="color: #FF8000">Messi! Messi! Messi!</h4>
        <p>
            Another thing that stands out is to be seen if you take a look at
            the graph with only the Person entities(You can do that in the
            settings menu). If you then take a look at the center of the graph
            you can see very clearly, that in the middle of all the discussions
            there is Messi. This puts the found clusters in some perspective, as
            it shows that the main discussed topic was indeed football and not
            anything political.
        </p>
    </li>
</ul>
<p>
    So it seems like our findings from the word graph have been confirmed by
    this graph. There is not too much additional information to be found.
</p>
<Modal
        isOpen={controlsAreOpen}
        toggle={() => (controlsAreOpen = !controlsAreOpen)}
>
    <div id="graph-chooser" style="margin: 2em">
        <Form>
            <legend>Filtering</legend>
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
                <Label>Entity types</Label>
                {#each Array.from(neTypeSelection.keys()) as neType}
                    <Input
                            id={neType + "cx"}
                            type="checkbox"
                            label={neType}
                            on:input={() => {
                            neTypeSelection.set(
                                neType,
                                !neTypeSelection.get(neType)
                            );
                            neTypeSelection = neTypeSelection;
                        }}
                            checked={neTypeSelection.get(neType)}
                    />
                {/each}
            </FormGroup>
        </Form>
        <Form>
            <legend>Clustering</legend>
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
        </Form>
        <Button
                type="button"
                on:click={() => rebuildGraph()}>Rebuild Graph
        </Button
        >
        {#if loading}
            <Loading displayString="graph"/>
        {/if}
        <p>
            <br/>
            <Icon name="exclamation-octagon-fill" class="hint"/>
            Note: We
            provided files for the unclustered graph in the following configurations:
            <br/>1. 10000 Edges
            <br/>2. 25000 Edges
            <br/>Graphs with the other number of Edges can be generated,
            however this could take a while. Applying custom clustering(only
            changing 'Clustering' settings) should be viable and normally should
            not take too long.
        </p>
    </div>
</Modal>

<style lang="scss">
  #sigma-container2 {
    width: 100%;
    height: 41em;
    margin: 0;
    padding: 0;
    overflow: hidden;
    margin-right: 2em;
  }

  #graph-container2 {
    display: flex;
    justify-content: space-around;
  }

  #cluster-div2 {
    min-width: 25em;
  }
</style>
