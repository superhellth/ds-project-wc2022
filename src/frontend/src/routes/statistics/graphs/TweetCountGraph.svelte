<script lang="ts">
    import { Chart } from "chart.js/auto";
    import ChartCard from "src/svelte-components/ChartCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { onMount } from "svelte";
    import { Col, Input, Row } from "sveltestrap";

    // data
    let elasticProvider: ElasticProvider = ElasticProvider.getInstance();
    let tweetsByDayPromise: Promise<Map<Date, number>> =
        elasticProvider.getTweetsByDayStats();

    // Chart
    let chart: Chart;
    let data: any = null;
    const chart_id = "c1";
    let header = "Tweets per Day";
    let footer = "As we can see in this graph...";
    let isBar: boolean = true;

    function setupChart(canvas_id: any, type: any, data: any): Chart {
        let chart = new Chart(canvas_id, {
            type: type,
            data: data,
        });

        return chart;
    }

    function onLineToggle() {
        isBar = !isBar;

        chart.destroy();
        chart = setupChart(
            chart_id,
            isBar ? 'bar' : 'line',
            data
        );
    }

    onMount(async () => {
        let tweetsByDayStats: Map<Date, number> = await tweetsByDayPromise;
        data = {
            labels: Array.from(tweetsByDayStats.keys()).map((date) =>
                date.toLocaleDateString("short")
            ),
            datasets: [
                {
                    label: "Tweets",
                    data: Array.from(tweetsByDayStats.values()),
                },
            ],
        };
        chart = setupChart(chart_id, "bar", data);
    });
</script>

{#await tweetsByDayPromise}
    <Loading displayString="Graph"/>
{:then ignored}
    <ChartCard {header} {footer} {chart_id}>
        <div slot="card-header-controls">
            <Row>
                <Col>
                    <Input
                        type="switch"
                        label="Line Graph"
                        on:input={onLineToggle}
                    />
                </Col>
            </Row>
        </div>
    </ChartCard>
{/await}
