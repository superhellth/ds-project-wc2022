<script lang="ts">
    import Label from "@smui/list/src/Label.svelte";
    import Loading from "src/svelte-components/Loading.svelte";
    import GenerateTweetProvider from "src/typescript/api_connections/generateTweetConnection";
    import {onMount} from "svelte";
    import {Breadcrumb, BreadcrumbItem, Button, Col, Form, FormGroup, Input, Row, Tooltip} from "sveltestrap";
    import {fly} from "svelte/transition";
    import TweetCard from "../../svelte-components/TweetCard.svelte";
    import Tweet from "../../typescript/tweet_management/tweet";
    import TwitterUser from "../../typescript/tweet_management/twitter-user";

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
    let tweetsGPT: Array<Tweet> = [];
    let amountTweets: number = 4;
    let temperature: number = 0.7;
    let repetition_penalty: number = 1.2;
    let length_penalty: number = 1.2;
    let showTooltipGPT: boolean = false;
    let loadingGPT: boolean = false;

    let innerNGram: HTMLTextAreaElement;
    let innerGPT: HTMLTextAreaElement;
    const twitterUser: TwitterUser = new TwitterUser(new Date(), "tsr", "rst", "rst", "Best User Ever",
        "https://i0.wp.com/pbs.twimg.com/media/Efso_-yUwAAJpRV.jpg", 0, 0, 0, 0, "trs", "bestusernameever", false);

    const resize = () => {
        innerNGram.style.height = "auto";
        innerNGram.style.height = 100 + innerNGram.scrollHeight + "px";
    };
    async function completeTweetNGram() {
        if (textNGram.split(" ").length >= n - 1) {
            loadingNGram = true;
            textNGram = await provider.getCompletedTweet(
                textNGram,
                tweetLength,
                n,
                topPercentage,
                allowRepition
            );
            loadingNGram = false;
        }
    }

    async function completeTweet() {
        loadingGPT = true;
        let tweet_texts = await provider.getFineTunedTweets(textGPT, temperature.toString(), repetition_penalty.toString(),
            length_penalty.toString(), amountTweets.toString());
        for (let i = 0; i < tweet_texts.length; i++) {
            tweetsGPT.push(new Tweet("", twitterUser, new Date(), "", "", "", false, 0, 0, 0, 0, tweet_texts[i], 0));
        }
        tweetsGPT = tweetsGPT;
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

<title>Experimental - Generate Tweet</title>
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
                    bind:inner={innerNGram}
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
                        <Button type="button" id="complete-button" on:click={() => completeTweetNGram()}
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
                <p style="color: red">In the docker version of this page, you can only choose n=1, because the other n-gram files would be too large.</p>
            </div>
        </Form>

        <Form>
            <h3>Tweet completion using Fine Tuned GPT-Neo model</h3>
            <FormGroup label="Enter your Prompt">
                <Input
                        id="tweet-input-gptneo"
                        bind:value={textGPT}
                        bind:inner={innerGPT}
                        on:input={resize}
                />
            </FormGroup>
            <p>
                We used the python library 'aitextgen' which is a wrapper for finetuning language models. To finetune,
                we used the GPT-neo model with 125m parameters
                (<a href="https://huggingface.co/EleutherAI/gpt-neo-125M?text=Messi+is">Link</a>) since it was the
                largest model that we could fine tune given the 10GB VRAM limitation of the used GPU. Finding proper
                tweets to feed into the model proofed to be difficult. Not properly understanding what actually happened
                in the background of the learning process didn't help either.
            </p>
            <p>
                Because of these reasons we moved the tweet generation to the experimental section of our project.
                <br>
                Anyways, enjoy! A good starting point would be 'Messi is'. This seems to generate decent results (well,
                at least sometimes^^).
            </p>
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
                    <Label for="temperature-select">Temperature</Label>
                    <Input
                            type="select"
                            name="select"
                            id="temperature-select"
                            bind:value={temperature}
                    >
                        {#each [0.5, 0.7, 1, 1.2] as n_}
                            <option>{n_}</option>
                        {/each}
                    </Input>
                </Form>
                <Form style="margin-left: 2em">
                    <Label for="repetition-select">Repetition Penalty</Label>
                    <Input
                            type="select"
                            name="select"
                            id="repetition-select"
                            bind:value={repetition_penalty}
                    >
                        {#each [0.7, 1, 1.2, 1.5] as n_}
                            <option>{n_}</option>
                        {/each}
                    </Input>
                </Form>
                <Form style="margin-left: 2em">
                    <Label for="length-select">Length Penalty</Label>
                    <Input
                            type="select"
                            name="select"
                            id="length-select"
                            bind:value={length_penalty}
                    >
                        {#each [0.7, 1, 1.2, 1.5] as n_}
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
                        May take some time.
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
                        <TweetCard
                                data={t}
                                showDetails={false}
                                sentimentMethod="None"
                                sentimentMethodIndex={-1}
                                sentimentScore="1"
                        />
                    </Col>
                {/each}
            </Row>
        </Form>
        <Form>
            <p>
                Sources: (Very authentic) profile picture from (https://i0.wp.com/pbs.twimg.com/media/Efso_-yUwAAJpRV.jpg [Accessed: 26.02.2023])
            </p>
        </Form>
    </FormGroup>
</div>