<script lang="ts">
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import Loading from "src/svelte-components/Loading.svelte";
    import { onMount } from "svelte";
    import { Table } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();

    let dataPromise: any = provider.getTopKUnigrams(10);

    let unigrams: Map<string, number> = new Map<string, number>;

    async function buildMap(): Promise<any> {
        let data = await dataPromise;
        console.log(data)
        for (const token in data) {
            unigrams.set(token, data[token])
        }

        console.log(unigrams)
        return true;
    }

    let readyPromise = buildMap();
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
            {#each Array.from(unigrams.keys()) as token, i}
                <tr>
                    <th scope="row">{i + 1}</th>
                    <td>{token}</td>
                    <td>{unigrams.get(token)}</td>
                </tr>
            {/each}
        </tbody>
    </Table>
{/await}
