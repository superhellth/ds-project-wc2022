<script lang="ts">
    import TopBar from "../../svelte-components/TopBar.svelte";
    import NavDrawer from "../../svelte-components/NavDrawer.svelte";
    let navDrawerIsOpen = false;
</script>

<TopBar bind:open={navDrawerIsOpen} path="/tweet-overview" />
<NavDrawer bind:open={navDrawerIsOpen} />
