<script lang="ts">
    import { Table } from "sveltestrap";

    export let map: Map<string, number>;
    export let keyColumnName: string;

    function getSortedArray() {
        return Array.from(map.keys()).sort(
            (a, b) => (map.get(b) || 0) - (map.get(a) || 0)
        );
    }
</script>

<div>
    <Table hover striped responsive>
        <thead>
            <tr>
                <th>#</th>
                <th>{keyColumnName}</th>
                <th>Count</th>
            </tr>
        </thead>
        <tbody>
            {#each getSortedArray() as key, i}
                <tr>
                    <th scope="row">{i + 1}</th>
                    <td>{key}</td>
                    <td>{map.get(key)}</td>
                </tr>
            {/each}
        </tbody>
    </Table>
</div>

<style>
    div {
        max-height: 35em;
        overflow: scroll;
    }
</style>