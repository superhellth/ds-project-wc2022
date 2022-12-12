<script lang="ts">
    // This is just a test if we can use chart.js charts inside this application
    // It makes use of the new ChartCart.svelte template for Charts/Graphs.

    import Layout from "../../svelte-components/Layout.svelte";
    import Chart from 'chart.js/auto';
    import {onMount} from "svelte";
    import {Button, Col, Container, Input, Row} from 'sveltestrap';
    import ChartCard from "../../svelte-components/ChartCard.svelte";


    const data = {
        labels: ['January', 'February', 'March', 'April', 'May', 'June'],
        datasets: [
            {
                label: 'Sales',
                data: [35, 45, 55, 65, 75, 85]
            }
        ]
    };

    let myChart;
    const chart_canvas_id = 'chart';
    let header = "Bar Chart Example"
    let footer = "Some additional information"

    function setupChart() {
        myChart = new Chart(chart_canvas_id, {
            type: 'bar',
            data: data
        });
    }

    onMount(setupChart)
</script>


<Layout>
    <Container>
        <Row>
            <Col>
                <ChartCard {header} {footer} chart_id={chart_canvas_id}>
                    <div slot="card-header-controls">
                        <Button>
                            I'm a button!
                        </Button>
                        <Input>
                            ...
                        </Input>
                    </div>
                </ChartCard>
            </Col>
            <Col>
                Some Text.
            </Col>
        </Row>
    </Container>
</Layout>
