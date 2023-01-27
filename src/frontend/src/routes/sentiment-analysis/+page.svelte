<script lang="ts">
    import Loading from "src/svelte-components/Loading.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { onMount } from "svelte";
    import { Button, Form, FormGroup, Input, Tooltip } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();

</script>

<title>Text Analytics - Sentiment Analysis</title>

<div>

</div>
