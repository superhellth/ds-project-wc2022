<script lang="ts">
    import IconButton from '@smui/icon-button';
    export let open = false;
    export let path = "/";
</script>


    <div id="header-container">
            <IconButton class="material-icons" on:click={() => open = !open}>menu</IconButton>
        <div>
            <p>{path}</p>
        </div>
    </div>


<style>
    #header-container {
        height: 3em;
        width: 100%;
        margin: 0;
        display: flex;
        background-color: grey;
    }
</style>