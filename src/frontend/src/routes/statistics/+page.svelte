<script lang="ts">
    // This is just a test if we can use chart.js charts inside this application
    // It makes use of the new ChartCart.svelte template for Charts/Graphs.

    import Layout from "../../svelte-components/Layout.svelte";
    import Chart from "chart.js/auto";
    import { onMount } from "svelte";
    import { Button, Col, Container, Input, Row } from "sveltestrap";
    import ChartCard from "../../svelte-components/ChartCard.svelte";
    import ElasticProvider from "../../typescript/api_connections/elasticProvider";

    // const data = {
    //     labels: ["January", "February", "March", "April", "May", "June"],
    //     datasets: [
    //         {
    //             label: "Sales",
    //             data: [35, 45, 55, 65, 75, 85],
    //         },
    //     ],
    // };
    // let myChart;
    // const chart_canvas_id = "chart";

    let elasticProvider: ElasticProvider = ElasticProvider.getInstance();
    let tweetsByDayPromise: Promise<Map<Date, number>> =
    elasticProvider.getTweetsByDayStats();
    let tweetsByDayChart: Chart;
    let aData: any = null;
    const tweets_by_days_canvas = "c1";
    let isBar: boolean = true;
    let header = "Tweets per Day";
    let footer = "As we can see in this graph...";

    function setupChart(canvas_id: any, type: any, data: any): Chart {
        let chart = new Chart(canvas_id, {
            type: type,
            data: data,
        });

        return chart;
    }

    function onLineToggle() {
        isBar = !isBar;

        tweetsByDayChart.destroy();
        tweetsByDayChart = setupChart(tweets_by_days_canvas, isBar ? "bar" : "line", aData)
    }


    onMount(async () => {
        // setupChart(chart_canvas_id, "bar", data);
        let tweetsByDayStats: Map<Date, number> = await tweetsByDayPromise;
        aData = {
            labels: Array.from(tweetsByDayStats.keys()).map(date => date.toLocaleDateString('short')),
            datasets: [
                {
                    label: "Tweets",
                    data: Array.from(tweetsByDayStats.values()),
                },
            ],
        };
        tweetsByDayChart = setupChart(tweets_by_days_canvas, "bar", aData);
    });
</script>

<Layout>
    <!-- <Container>
        <Row>
            <Col>
                <ChartCard {header} {footer} chart_id={chart_canvas_id}>
                    <div slot="card-header-controls">
                        <Row>
                            <Col>
                                <Button on:click={() => console.log("Button 1 pressed")}>
                                    Button 1
                                </Button>
                            </Col>
                            <Col>
                                <Button on:click={() => console.log("Button 2 pressed")}>
                                    Button 2
                                </Button>
                            </Col>
                            <Col>
                                <Button on:click={() => console.log("Button 3 pressed")}>
                                    Button 3
                                </Button>
                            </Col>
                        </Row>
                    </div>
                </ChartCard>
            </Col>
            <Col>
                Some Text.
            </Col>
        </Row>
    </Container> -->
    {#await tweetsByDayPromise}
        <p>Loading...</p>
    {:then ignored}
        <ChartCard {header} {footer} chart_id={tweets_by_days_canvas}>
            <div slot="card-header-controls">
                <Row>
                    <Col>
                        <Input id="bar-line-toggle" type="switch" label="Line Graph" on:input={onLineToggle}/>
                    </Col>
                </Row>
            </div>
        </ChartCard>
    {/await}
</Layout>
