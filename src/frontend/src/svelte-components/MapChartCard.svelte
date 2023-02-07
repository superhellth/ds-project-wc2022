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

    let backgroundColors: string[] = [
        "rgba(255, 99, 132)",
        "rgba(255, 159, 64)",
        "rgba(255, 205, 86)",
        "rgba(75, 192, 192)",
        "rgba(54, 162, 235)",
        "rgba(153, 102, 255)",
        "rgba(201, 203, 207)",
    ];

    function shuffleArray(array: any[]) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    onMount(async () => {
        let chartData = {
            labels: Array.from(dataMap.keys()),
            datasets: [
                {
                    label: "Tweets",
                    data: Array.from(dataMap.values()),
                    backgroundColor: shuffleArray(backgroundColors),
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
    <Loading displayString="Graph" />
{:then ignored}
    <ChartCard {header} {footer} chart_id={chartID} />
{/await}
