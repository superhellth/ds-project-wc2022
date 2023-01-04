<script lang="ts">
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import Loading from "src/svelte-components/Loading.svelte";
    import { onMount } from "svelte";
    import { Col, Dropdown, Input, Row, Table } from "sveltestrap";
    import CountTable from "src/svelte-components/CountTable.svelte";
    import BasicCard from "src/svelte-components/BasicCard.svelte";

    let provider: ElasticProvider = ElasticProvider.getInstance();

    async function buildMaps(): Promise<any> {
        let tokens = await tokenPromise;
        let mentions = await mentionPromise;
        let hashtags = await hashtagPromise;

        tokenMap = new Map<string, number>();
        mentionMap = new Map<string, number>();
        hashtagMap = new Map<string, number>();

        for (const token in tokens) {
            tokenMap.set(token, tokens[token]);
        }
        for (const token in mentions) {
            mentionMap.set(token, mentions[token]);
        }
        for (const token in hashtags) {
            hashtagMap.set(token, hashtags[token]);
        }

        return true;
    }

    let options = [3, 10, 20, 50, 100];
    let numTokens = 10;
    let numMentions = 10;
    let numHashtags = 10;

    let tokenPromise: any = provider.getTopKUnigrams(
        numTokens,
        false,
        false,
        false
    );
    let mentionPromise: any = provider.getTopKUnigrams(
        numMentions,
        false,
        true,
        false
    );
    let hashtagPromise: any = provider.getTopKUnigrams(
        numHashtags,
        false,
        false,
        true
    );

    $: {
        tokenPromise = provider.getTopKUnigrams(numTokens, false, false, false);
        mentionPromise = provider.getTopKUnigrams(
            numMentions,
            false,
            true,
            false
        );
        hashtagPromise = provider.getTopKUnigrams(
            numHashtags,
            false,
            false,
            true
        );
        readyPromise = buildMaps();
    }

    let tokenMap: Map<string, number>;
    let mentionMap: Map<string, number>;
    let hashtagMap: Map<string, number>;

    let readyPromise = buildMaps();
</script>

<title>Statistics - Hashtags and Mentions</title>

{#await readyPromise}
    <Loading displayString="Unigrams" />
{:then ignored}
    <Row>
        <Col>
            <BasicCard header="Common Tokens" footer="Here we can see...">
                <div slot="card-header-controls">
                    <Input
                        color="dark"
                        type="select"
                        name="select"
                        id="exampleSelect"
                        style="width: 5em"
                        bind:value={numTokens}
                    >
                        {#each options as option}
                            <option>{option}</option>
                        {/each}
                    </Input>
                </div>
                <CountTable map={tokenMap} keyColumnName="Token" slot="body" />
            </BasicCard>
        </Col>
        <Col>
            <BasicCard header="Common Mentions" footer="This shows...">
                <div slot="card-header-controls">
                    <Input
                        color="dark"
                        type="select"
                        name="select"
                        id="exampleSelect"
                        style="width: 5em"
                        bind:value={numMentions}
                    >
                        {#each options as option}
                            <option>{option}</option>
                        {/each}
                    </Input>
                </div>
                <CountTable
                    map={mentionMap}
                    keyColumnName="Mention"
                    slot="body"
                />
            </BasicCard>
        </Col>
        <Col>
            <BasicCard header="Common Hashtags" footer="bla bla bla">
                <div slot="card-header-controls">
                    <Input
                        color="dark"
                        type="select"
                        name="select"
                        id="exampleSelect"
                        style="width: 5em"
                        bind:value={numHashtags}
                    >
                        {#each options as option}
                            <option>{option}</option>
                        {/each}
                    </Input>
                </div>
                <CountTable
                    map={hashtagMap}
                    keyColumnName="Hashtag"
                    slot="body"
                />
            </BasicCard>
        </Col>
    </Row>
{/await}
