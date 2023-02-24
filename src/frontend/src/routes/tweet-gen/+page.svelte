<script lang="ts">
    import Label from "@smui/list/src/Label.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import GenerateTweetProvider from "src/typescript/api_connections/generateTweetConnection";
    import {onMount} from "svelte";
    import {Alert, Breadcrumb, BreadcrumbItem, Button, Col, Form, FormGroup, Input, Row, Tooltip} from "sveltestrap";
    import {fly} from "svelte/transition";

    // NGram variables
    let provider: GenerateTweetProvider = GenerateTweetProvider.getInstance();
    let textNGram: string = "";
    let n: number = 3;
    let tweetLength: number = 10;
    let topPercentage: number = 0.5;
    let loadingNGram: boolean = false;
    let allowRepition: boolean = false;

    let showTooltipNGram: boolean = false;

    // GPT variables
    let textGPT: string = "";
    let tweetsGPT: Array<string> = [];
    let amountTweets: number = 4;
    let showTooltipGPT: boolean = false;
    let loadingGPT: boolean = false;

    let innerNGram: HTMLTextAreaElement;
    let innerGPT: HTMLTextAreaElement;
    const resize = () => {
        innerNGram.style.height = "auto";
        innerGPT.style.height = "auto";
        innerNGram.style.height = 100 + innerNGram.scrollHeight + "px";
        innerGPT.style.height = 100 + innerGPT.scrollHeight + "px";
    };
    // async function completeTweet() {
    //     if (text.split(" ").length >= n - 1) {
    //         loading = true;
    //         textNGram = await provider.getCompletedTweet(
    //             textNGram,
    //             tweetLength,
    //             n,
    //             topPercentage,
    //             allowRepition
    //         );
    //         loading = false;
    //     }
    // }

    async function completeTweet() {
        loadingGPT = true;
        tweetsGPT = await provider.getFineTunedTweets(textGPT, amountTweets.toString());
        loadingGPT = false;
    }

    onMount(async () => {
        resize();
        let queryInput = document.getElementById("tweet-input")!;
        queryInput.style.backgroundColor = "#212529";
        queryInput.style.color = "#FFFFFF";
        queryInput = document.getElementById("tweet-input-gptneo")!;
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

<div in:fly={{ y: 2500, duration: 1000, delay: 0 }}>
    <FormGroup>
        <Form>
            <h3>Tweet completion using n-grams</h3>
            <Input
                    id="tweet-input"
                    type="textarea"
                    bind:value={textNGram}
                    bind:innerNGram
                    on:input={resize}
            />
            <div>
                <Form inline>
                    <Form>
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
                    </Form>
                    <Form style="margin-left: 2em">
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
                    </Form>
                    <Form style="margin-left: 2em">
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
                    </Form>
                    <Form style="margin-left: 2em">
                        <Label>Allow repition of n-grams</Label>
                        <Input type="switch" label="yes" bind:checked={allowRepition}/>
                    </Form>
                    <Form style="margin-left: 2em">
                        <Label>Complete Tweet</Label>
                        <Button type="button" id="complete-button" on:click={() => completeTweet()}
                        >Complete
                        </Button
                        >
                        <Tooltip bind:isOpen={showTooltipNGram} placement="right" target="complete-button">
                            Only works if n-1 words were typed.
                        </Tooltip>
                    </Form>
                    {#if loadingNGram}
                        <div style="margin-left: 8em">
                            <Loading displayString="completed Tweet"/>
                        </div>
                    {/if}
                </Form>
                <p>
                    Note: The higher the % of n-grams to consider, the better the
                    result, though the performance might worsen significantly.
                    <br/> Combining a high tweet length, high n-gram size and high % of
                    n-grams to consider with the disallowance of repitition often leads
                    to very long waiting times.
                    <br/> Also note that the first tweet generated for each n-gram size
                    is always the slowest, since the n-grams have to be loaded from file.
                </p>
            </div>
        </Form>

        <Form>
            <h3>Tweet completion using Fine Tuned GPT-Neo model</h3>
            <FormGroup label="Enter your Prompt">
                <Input
                        id="tweet-input-gptneo"
                        bind:value={textGPT}
                        bind:innerGPT
                        on:input={resize}
                />
            </FormGroup>
            <Form inline>
                <Form>
                    <Label for="amount-tweet-select">Amount of Tweets</Label>
                    <Input
                            type="select"
                            name="select"
                            id="amount-tweet-select"
                            bind:value={amountTweets}
                    >
                        {#each [4, 8, 12] as n_}
                            <option>{n_}</option>
                        {/each}
                    </Input>
                </Form>
                <Form style="margin-left: 2em">
                    <Label>Complete Tweet</Label>
                    <Button type="button" id="complete-gpt-tweet-button" on:click={() => completeTweet()}
                    >Complete
                    </Button
                    >
                    <Tooltip bind:isOpen={showTooltipGPT} placement="right" target="complete-gpt-tweet-button">
                        May need some time.
                    </Tooltip>
                </Form>
                {#if loadingGPT}
                    <div style="margin-left: 8em">
                        <Loading displayString="completed Tweet"/>
                    </div>
                {/if}
            </Form>
        </Form>
        <Form>
            <br>
            <Row cols={{ xl: 4, lg: 3, md: 2, sm: 1 }}>
                {#each tweetsGPT as t}
                    <Col>
                        <Alert color="primary">
                            <h5 style="color: black">Tweet</h5>
                            {t}
                        </Alert>
                    </Col>
                {/each}
            </Row>
        </Form>
    </FormGroup>
</div>