<script lang="ts">
    import { Chart } from "chart.js/auto";
    import ChartCard from "src/svelte-components/ChartCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import { onMount } from "svelte";

    // Chart
    let chart: any;
    export let chartID = "c1";
    export let header = "Tweets per Day";
    export let footer = "As we can see in this graph...";
    export let dataMap: Map<string, number>;
    export let type: any = "pie";

    onMount(async () => {
        let chartData = {
            labels: Array.from(dataMap.keys()),
            datasets: [
                {
                    label: "Tweets",
                    data: Array.from(dataMap.values()),
                },
            ],
        };
        chart = new Chart(chartID, {
            type: type,
            data: chartData,
        });

        return true;
    });
</script>

{#await onMount}
    <Loading displayString="Graph"/>
{:then ignored}
    <ChartCard {header} {footer} chart_id={chartID} />
{/await}