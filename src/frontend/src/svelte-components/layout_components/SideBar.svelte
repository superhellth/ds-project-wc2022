<script lang="ts">
    import Nav from "sveltestrap/src/Nav.svelte";
    import SidebarItem from "./SidebarItem.svelte";

    export let theme: any;
    export let isOpen: boolean = true;

    $: sidenav_theme = `sb-sidenav-${theme}`;
</script>

<div id="layoutSidenav_nav" class="sb-nav-fixed">
    <Nav
        class="sb-sidenav {sidenav_theme} accordion sb-nav-fixed"
        id="sidenavAccordion"
        style="background-color: var(--side-bar-color)"
    >
        <div class="sb-sidenav-menu">
            <Nav>
                <div
                    class="sb-sidenav-menu-heading"
                >
                    Overview
                </div>
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Home"
                    href="/"
                    iconName="house-heart-fill"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Twitter Feed"
                    href="/overview"
                    iconName="twitter"
                />

                <div class="sb-sidenav-menu-heading">Statistics</div>
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Collected Data"
                    href="/statistics"
                    iconName="graph-up"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Unigrams insights"
                    href="/unigram-insights"
                    iconName="input-cursor-text"
                />
                <div class="sb-sidenav-menu-heading">Text Analytics</div>
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Word Graph"
                    href="/word-graph"
                    iconName="bounding-box"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Named entity Graph"
                    href="/ne-graph"
                    iconName="bounding-box"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Sentiment Analysis"
                    href="/sentiment-analysis"
                    iconName="emoji-smile-upside-down"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Word embeddings"
                    href="/word-embedding"
                    iconName="body-text"
                />
                <div class="sb-sidenav-menu-heading">Experimental</div>
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Tweet Generation"
                    href="/tweet-gen"
                    iconName="chat-text"
                />
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Scrap Yard"
                    href="/scrap-yard"
                    iconName="trash"
                />
                <div class="sb-sidenav-menu-heading">Settings</div>
                <SidebarItem
                    on:press={() => {
                        theme = "dark";
                    }}
                    text="Stream control"
                    href="/settings"
                    iconName="gear"
                />
            </Nav>
        </div>
    </Nav>
</div>
