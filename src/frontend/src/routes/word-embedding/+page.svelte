<script lang="ts">
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Form, FormGroup, Input, Label } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let checkIfExistsString: string = "Christiano Ronaldo";
    let checkIfExistsValue: boolean = false;
    let doesntMatchString: string =
        "Lionel Messi, Phil Foden, Kyle Walker, Declan Rice, Harry Kane";
    let doesntMatchValue: string = "";
    let x1: string = "Hansi Flick";
    let y1: string = "Germany";
    let x2: string = "Didier Deschamps";
    let y2: string = "";

    $: {
        checkIfExists(checkIfExistsString);
    }

    async function checkIfExists(checkIfExistsString: string) {
        checkIfExistsValue = await provider.existsInW2vecVocabulary(
            checkIfExistsString.trim().replaceAll(" ", "_").toLowerCase()
        );
    }

    $: {
        doesNotMatch(doesntMatchString);
    }

    async function doesNotMatch(doesntMatchString: string) {
        let words: string[] = doesntMatchString.split(",");
        for (let i = 0; i < words.length; i++) {
            words[i] = words[i].trim().replaceAll(" ", "_").toLocaleLowerCase();
        }
        let res = await provider.doesntMatch(words);
        doesntMatchValue = res.replaceAll("_", " ");
    }

    $: {
        x1IsToy2Likex2IsTo(x1, y1, x2);
    }

    async function x1IsToy2Likex2IsTo(x1: string, y1: string, x2: string) {
        let res = await provider.getSimilar(
            [
                x2.trim().replaceAll(" ", "_").toLocaleLowerCase(),
                y1.trim().replaceAll(" ", "_").toLocaleLowerCase(),
            ],
            [x1.trim().replaceAll(" ", "_").toLocaleLowerCase()]
        );
        y2 = res[0];
    }
</script>

<title>Text Analytics - Word2Vec</title>

<h2>Word2Vec Embedding</h2>
<p>Our Embedding is a gensim Word2Vec Model trained on our whole corpus...</p>

<h3>Explore the embedding</h3>
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
    <Input type="text" bind:value={x1} />
    <Label style="margin: 5px">is to</Label>
    <Input type="text" bind:value={y1} />
    <Label style="margin: 5px">like</Label>
    <Input type="text" bind:value={x2} />
    <Label style="margin: 5px">is to</Label>
    <Input type="text" bind:value={y2} />
</Form>
