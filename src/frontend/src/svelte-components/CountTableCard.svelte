<script lang="ts">
    import CountTable from "./CountTable.svelte";
    import { Input } from "sveltestrap";
    import BasicCard from "./BasicCard.svelte";
    import Loading from "./Loading.svelte";

    export let providingFunction: (
        k: number,
        includeStopWords: boolean
    ) => Object;
    export let showStopWordSwitch: boolean = false;
    export let footer = "Lorem ipsum";
    export let header = "Lorem ipsum";

    let options = [3, 10, 20, 50, 100];
    let displayedRows = 10;
    let includeStopWords = false;
    let countMap: Map<string, number>;
    $: tokenPromise = providingFunction(displayedRows, includeStopWords);
    $: readyPromise = (async () => {
        countMap = new Map(Object.entries(await tokenPromise));
        return true;
    })();
</script>

{#await readyPromise}
    <Loading displayString={header} />
{:then ignored}
    <BasicCard {header} {footer}>
        <div slot="card-header-controls">
            <Input
                color="dark"
                type="select"
                name="select"
                style="width: 5em"
                bind:value={displayedRows}
            >
                {#each options as option}
                    <option>{option}</option>
                {/each}
            </Input>
            {#if showStopWordSwitch}
                <Input
                    id="c3"
                    type="switch"
                    label="Include Stop Words"
                    bind:checked={includeStopWords}
                />
            {/if}
        </div>
        <CountTable map={countMap} keyColumnName="Token" slot="body" />
    </BasicCard>
{/await}
