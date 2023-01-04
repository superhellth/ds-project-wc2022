<script lang="ts">
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import Loading from "src/svelte-components/Loading.svelte";
    import { onMount } from "svelte";
    import { Table } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();

    let tokenPromise: any = provider.getTopKUnigrams(10, false, false, false);
    let mentionPromise: any = provider.getTopKUnigrams(10, false, true, false)
    let hashtagPromise: any = provider.getTopKUnigrams(10, false, false, true)

    let tokenMap: Map<string, number> = new Map<string, number>;
    let mentionMap: Map<string, number> = new Map<string, number>;
    let hashtagMap: Map<string, number> = new Map<string, number>;

    async function buildMaps(): Promise<any> {
        let tokens = await tokenPromise;
        let mentions = await mentionPromise;
        let hashtags = await hashtagPromise;
        for (const token in tokens) {
            tokenMap.set(token, tokens[token])
        }
        for (const token in mentions) {
            mentionMap.set(token, mentions[token])
        }
        console.log(mentions)
        for (const token in hashtags) {
            hashtagMap.set(token, hashtags[token])
        }

        return true;
    }

    let readyPromise = buildMaps();
</script>

<title>Statistics - Hashtags and Mentions</title>

{#await readyPromise}
    <Loading displayString="Unigrams"/>
{:then ignored}
    <Table>
        <thead>
            <tr>
                <th>#</th>
                <th>Token</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {#each Array.from(tokenMap.keys()) as token, i}
                <tr>
                    <th scope="row">{i + 1}</th>
                    <td>{token}</td>
                    <td>{tokenMap.get(token)}</td>
                </tr>
            {/each}
        </tbody>
    </Table>
    <Table>
        <thead>
            <tr>
                <th>#</th>
                <th>Mention</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {#each Array.from(mentionMap.keys()) as token, i}
                <tr>
                    <th scope="row">{i + 1}</th>
                    <td>{token}</td>
                    <td>{mentionMap.get(token)}</td>
                </tr>
            {/each}
        </tbody>
    </Table>
    <Table>
        <thead>
            <tr>
                <th>#</th>
                <th>Hashtag</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {#each Array.from(hashtagMap.keys()) as token, i}
                <tr>
                    <th scope="row">{i + 1}</th>
                    <td>{token}</td>
                    <td>{hashtagMap.get(token)}</td>
                </tr>
            {/each}
        </tbody>
    </Table>
{/await}
