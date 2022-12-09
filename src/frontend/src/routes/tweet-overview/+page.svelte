<script lang="ts">
    import Layout from "../../svelte-components/Layout.svelte";
    import Chart from 'chart.js/auto';
    import {onMount} from "svelte";
    import {Card, CardBody, CardFooter, CardHeader, Col, Container, Icon, Row} from 'sveltestrap';


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

    function setupChart() {
        myChart = new Chart('bar-chart', {
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
            <Card>
                <CardHeader>
                    Some Header Text <Icon name="globe2" />
                </CardHeader>
                <CardBody>
                    <div>
                        <canvas id="bar-chart"></canvas>
                    </div>
                </CardBody>
                <CardFooter>Some Text as Footer</CardFooter>
            </Card>
        </Col>
    </Row>
    <Row>
        <Col>.col</Col>
        <Col>.col</Col>
        <Col>.col</Col>
        <Col>.col</Col>
    </Row>
</Container>
</Layout>


