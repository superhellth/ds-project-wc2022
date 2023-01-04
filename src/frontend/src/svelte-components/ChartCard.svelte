<script lang="ts">
    import BasicCard from "./BasicCard.svelte";

    // Add header, footer text and chart_id as variables that can be passed to the component
    export let header: string;
    export let footer: string;
    export let chart_id: any = "";
</script>

<BasicCard {header} {footer}>
    <div slot="card-header-controls"><slot name="card-header-controls" /></div>

    <div slot="body">
        <canvas id={chart_id} />
    </div>
</BasicCard>
