<script lang="ts">
    import CountTable from "src/svelte-components/CountTable.svelte";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Breadcrumb, BreadcrumbItem, Form, FormGroup, Input, Label } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let checkIfExistsString: string = "Christiano Ronaldo";
    let checkIfExistsValue: boolean = false;
    let doesntMatchString: string =
        "Lionel Messi, Phil Foden, Kyle Walker, Declan Rice, Harry Kane";
    let doesntMatchValue: string = "";
    let x1: string = "Hansi Flick";
    let x1IsValid: boolean = true;
    let y1: string = "Germany";
    let y1IsValid: boolean = true;
    let x2: string = "Didier Deschamps";
    let x2IsValid: boolean = true;
    let y2: any = [[]];

    $: {
        checkIfExists(checkIfExistsString);
    }

    async function checkIfExists(checkIfExistsString: string) {
        checkIfExistsValue = await provider.existsInW2vecVocabulary(
            preprocessString(checkIfExistsString)
        );
    }

    $: {
        doesNotMatch(doesntMatchString);
    }

    async function doesNotMatch(doesntMatchString: string) {
        let words: string[] = doesntMatchString.split(",");
        for (let i = 0; i < words.length; i++) {
            words[i] = preprocessString(words[i]);
        }
        let res = await provider.doesntMatch(words);
        doesntMatchValue = res.replaceAll("_", " ");
    }

    $: {
        x1IsToy2Likex2IsTo(x1, y1, x2);
    }

    async function x1IsToy2Likex2IsTo(x1: string, y1: string, x2: string) {
        x1IsValid = await provider.existsInW2vecVocabulary(
            preprocessString(x1)
        );
        y1IsValid = await provider.existsInW2vecVocabulary(
            preprocessString(y1)
        );
        x2IsValid = await provider.existsInW2vecVocabulary(
            preprocessString(x2)
        );
        if (x1IsValid && x2IsValid && y1IsValid) {
            y2 = await provider.getSimilar(
                [preprocessString(x2), preprocessString(y1)],
                [preprocessString(x1)]
            );
        }
    }

    function preprocessString(str: string): string {
        return str.trim().replaceAll(" ", "_").toLowerCase();
    }
</script>

<title>Text Analytics - Word2Vec</title>

<h1>Word2Vec Embedding</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Word2Vec</BreadcrumbItem>
</Breadcrumb>

<h3>Explore the embedding</h3>
<p>Our Embedding is a gensim Word2Vec Model trained on our whole corpus...</p>
<Form>
    <FormGroup>
        <Label>Check for embedding</Label>
        <Input
            type="text"
            bind:value={checkIfExistsString}
            valid={checkIfExistsValue}
            invalid={!checkIfExistsValue}
            feedback={checkIfExistsValue
                ? "Embedding exists"
                : "Embedding does not exist"}
        />
    </FormGroup>
    <FormGroup>
        <Label>Doesn't match</Label>
        <Input
            type="text"
            bind:value={doesntMatchString}
            feedback={doesntMatchValue + " does not match"}
            invalid={true}
        />
    </FormGroup>
</Form>
<Label>x is to y like z is to...</Label>
<Form inline>
    <Input type="text" bind:value={x1} valid={x1IsValid} invalid={!x1IsValid} />
    <Label style="margin: 5px">is to</Label>
    <Input type="text" bind:value={y1} valid={y1IsValid} invalid={!y1IsValid} />
    <Label style="margin: 5px">like</Label>
    <Input type="text" bind:value={x2} valid={x2IsValid} invalid={!x2IsValid} />
    <Label style="margin: 5px">is to</Label>
    <Input type="text" disabled bind:value={y2[0][0]} feedback={y2.slice(0, 3)} valid />
</Form>
