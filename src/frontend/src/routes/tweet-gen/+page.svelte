<script lang="ts">
    import Label from "@smui/list/src/Label.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { onMount } from "svelte";
    import { Breadcrumb, BreadcrumbItem, Button, Form, FormGroup, Input, Tooltip } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let text: string = "";
    let n: number = 3;
    let tweetLength: number = 10;
    let topPercentage: number = 0.5;
    let loading: boolean = false;
    let allowRepition: boolean = false;

    let showTooltip: boolean = false;

    let inner: HTMLTextAreaElement;
    const resize = () => {
        inner.style.height = "auto";
        inner.style.height = 100 + inner.scrollHeight + "px";
    };
    async function completeTweet() {
        if (text.split(" ").length >= n - 1) {
            loading = true;
            text = await provider.getCompletedTweet(
                text,
                tweetLength,
                n,
                topPercentage,
                allowRepition
            );
            loading = false;
        }
    }

    onMount(async () => {
        resize();
        let queryInput = document.getElementById("tweet-input")!;
        queryInput.style.backgroundColor = "#212529";
        queryInput.style.color = "#FFFFFF";
    });
</script>

<title>Text Analytics - Generate Tweet</title>
<h1>Tweet Completion</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Tweet Completion</BreadcrumbItem>
</Breadcrumb>

<div>
    <FormGroup>
        <h3>Start writing a Tweet</h3>
        <Input
            id="tweet-input"
            type="textarea"
            bind:value={text}
            bind:inner
            on:input={resize}
        />
    </FormGroup>
    <div style="float: left">
        <Form inline>
            <FormGroup>
                <Label for="n-gram-select">n-gram-size</Label>
                <Input
                    type="select"
                    name="select"
                    id="n-gram-select"
                    bind:value={n}
                >
                    {#each [1, 2, 3, 4] as n_}
                        <option>{n_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup style="margin-left: 2em">
                <Label for="tweet-length-select">Tweet length</Label>
                <Input
                    type="select"
                    name="select"
                    id="tweet-length-select"
                    bind:value={tweetLength}
                >
                    {#each [10, 20, 30] as tweetSize_}
                        <option>{tweetSize_}</option>
                    {/each}
                </Input>
            </FormGroup>
            <FormGroup style="margin-left: 2em">
                <Label for="top-n-grams-range">% of n-grams to consider</Label>
                <Input
                    type="range"
                    name="range"
                    id="top-n-grams-range"
                    min={0}
                    max={1}
                    step={0.01}
                    bind:value={topPercentage}
                />
            </FormGroup>
            <FormGroup style="margin-left: 2em">
                <Label>Allow repition of n-grams</Label>
                <Input type="switch" label="yes" bind:checked={allowRepition} />
            </FormGroup>
            <FormGroup style="margin-left: 2em">
                <Label>Complete Tweet</Label>
                <Button type="button" id="complete-button" on:click={() => completeTweet()}
                    >Complete</Button
                >
                <Tooltip bind:isOpen={showTooltip} placement="right" target="complete-button">
                    Only works if n-1 words were typed.
                  </Tooltip>
            </FormGroup>
            {#if loading}
                <div style="margin-left: 8em">
                    <Loading displayString="completed Tweet" />
                </div>
            {/if}
        </Form>
        <p>
            Note: The higher the % of n-grams to consider, the better the
            result, though the performance might worsen significantly.
            <br /> Combining a high tweet length, high n-gram size and high % of
            n-grams to consider with the disallowance of repitition often leads
            to very long waiting times.
            <br /> Also note that the first tweet generated for each n-gram size
            is always the slowest, since the n-grams have to be loaded from file.
        </p>
    </div>
</div>
