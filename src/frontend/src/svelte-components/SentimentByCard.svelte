<script lang="ts">
    import {Chart} from "chart.js/auto";
    import ChartCard from "src/svelte-components/ChartCard.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import {onMount} from "svelte";
    import MiddlewareProvider from "../typescript/api_connections/middlewareConnection";
    import {Col, FormGroup, Input, Label, Row} from "sveltestrap";

    // Chart
    export let chart_id = "c2";
    export let header = "Tweets per Day";
    export let footer = "As we can see in this graph...";
    let useMethodVsSent = false;
    let useMethodBertSent = true;
    let useMethodLrcOwn = true;
    let useMethodLrcOther = false;
    let byTime;
    let chart;

    // Data
    let provider: MiddlewareProvider = MiddlewareProvider.getInstance()
    let chartData;

    async function getChartData() {
        chartData = await provider.getSentimentOverTime();
    }

    async function updateChart() {
        await getChartData();

        let vsSentData = chartData[byTime['cmd']].map(d => d.vs_sent);
        let bertSentData = chartData[byTime.cmd].map(d => d.bert_sent);
        let lrcOwnData = chartData[byTime.cmd].map(d => d.lrc_own);
        let lrcOtherData = chartData[byTime.cmd].map(d => d.lrc_other);

        let datasets = [];
        if (useMethodVsSent) {
            datasets.push({
                borderColor: "#3e95cd",
                data: vsSentData,
                label: "VS Sent",
                fill: false
            });
        }
        if (useMethodBertSent) {
            datasets.push({
                borderColor: "#8e5ea2",
                data: bertSentData,
                label: "Bert Sent",
                fill: false
            });
        }
        if (useMethodLrcOwn) {
            datasets.push({
                borderColor: "#3cba9f",
                data: lrcOwnData,
                label: "LRC Own",
                fill: false
            });
        }
        if (useMethodLrcOther) {
            datasets.push({
                borderColor: "#e8c3b9",
                data: lrcOtherData,
                label: "LRC Other",
                fill: false
            });
        }

        if (chart) {
            chart.destroy();
        }

        chart = new Chart(chart_id, {
            type: "line",
            data: {
                labels: chartData[byTime.cmd].map(d => d.date),
                datasets
            },
            options: {
                responsive: true
            }
        });
    }

    onMount(async () => {
        await getChartData();
        await updateChart();
    });

</script>

{#await chartData}
    <Loading displayString="Graph"/>
{:then ignored}
    <ChartCard {header} {footer} {chart_id}>
        <div slot="card-header-controls">
            <div class="float-left">
                <Row>
                <Col>
                    <FormGroup style="margin-left: 2em">
                        <Label for="timeframe-select"><b>Timeframe selection</b></Label>
                        <Input
                            type="select"
                            id="timeframe-select"
                            on:change={() => updateChart()}
                            bind:value={byTime}
                        >
                        {#each [{id: 0, text: 'by Days', cmd: 'by_days'},
                                {id: 1, text: 'by Weeks', cmd: 'by_week'},
                                {id: 2, text: 'by Months', cmd: 'by_month'}] as timeframe}
                            <option value={timeframe}>{timeframe.text}</option>
                        {/each}
                    </Input>
                    </FormGroup>
                </Col>
                <Col>
                    <b class="inv">Sentiment methods</b>
                    <Row>
                    <Col>
                          <FormGroup>
                            <Input
                                    id="cvs"
                                    type="checkbox"
                                    label="vaderSentiment"
                                    bind:checked={useMethodVsSent}
                                    on:change={() => updateChart()}
                            />
                          </FormGroup>
                    </Col>
                    <Col>
                          <FormGroup>
                            <Input
                                    id="ccother"
                                    type="checkbox"
                                    label="SGDClassifierOther"
                                    bind:checked={useMethodLrcOther}
                                    on:change={() => updateChart()}
                            />
                          </FormGroup>
                    </Col>
                    <Col>
                          <FormGroup>
                            <Input
                                    id="ccown"
                                    type="checkbox"
                                    label="SGDClassifierOwn"
                                    bind:checked={useMethodLrcOwn}
                                    on:change={() => updateChart()}
                            />
                          </FormGroup>
                    </Col>
                    <Col>
                          <FormGroup>
                            <Input
                                    id="cbc"
                                    type="checkbox"
                                    label="BERT based Classifier"
                                    bind:checked={useMethodBertSent}
                                    on:change={() => updateChart()}
                            />
                          </FormGroup>
                    </Col>
                    </Row>
                </Col>
                </Row>
            </div>
        </div>
    </ChartCard>
{/await}
