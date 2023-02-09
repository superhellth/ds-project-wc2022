<script lang="ts">
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import {
        Breadcrumb,
        BreadcrumbItem,
        Form,
        FormGroup,
        Input,
        Label,
        Image,
        Progress,
    } from "sveltestrap";

    let provider: MiddlewareProvider = MiddlewareProvider.getInstance();

    let checkIfExistsString: string = "Human Rights";
    let checkIfExistsString2: string = "Qatar";
    let checkIfExistsValue: boolean = false;
    let checkIfExistsValue2: boolean = false;
    let numCloseWords: number = 20;
    let numCloseWords2: number = 20;
    let numFarWords: number = 0;
    let numFarWords2: number = 0;
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
        checkIfExists(checkIfExistsString, false);
        checkIfExists(checkIfExistsString2, true);
    }

    async function checkIfExists(checkIfExistsString: string, second: boolean) {
        if (second) {
            checkIfExistsValue = await provider.existsInW2vecVocabulary(
                preprocessString(checkIfExistsString)
            );
        } else {
            checkIfExistsValue2 = await provider.existsInW2vecVocabulary(
                preprocessString(checkIfExistsString)
            );
        }
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

<h3>Explore the Embedding</h3>
<p>
    Our Embedding is a gensim Word2Vec Model trained on our whole corpus. The
    training parameters have been finetuned to fit out corpus. Our dataset is
    big enough, that things like "Hansi Flick" - "Germany" + "France" = "Didier
    Deschamps" work. However our data is very football specific, so "King" -
    "Man" + "Woman" does not work quite as good.
</p>
<h4>Check for Embedding</h4>
{#if checkIfExistsValue && checkIfExistsValue2}
    {#await provider.getDistance(preprocessString(checkIfExistsString), preprocessString(checkIfExistsString2)) then distance}
        <div style="margin: 1em">
            <p style="margin: auto; width: 50%; text-align: center">Distance between Words: {distance}</p>
            <Progress value={100 - distance * 100} style="margin: auto; width: 50%;" />
        </div>
    {/await}
{/if}
<div style="display: flex; justify-content: space-evenly">
    <div>
        <Input
            type="text"
            bind:value={checkIfExistsString}
            valid={checkIfExistsValue}
            invalid={!checkIfExistsValue}
            feedback={checkIfExistsValue
                ? "Embedding exists"
                : "Embedding does not exist"}
        />
        {#if checkIfExistsValue}
            <img
                src={provider.getTSNEPlotURL(
                    preprocessString(checkIfExistsString),
                    numCloseWords,
                    numFarWords
                )}
                alt="plot"
                style="width: 27em; height: 27em"
            />
            <br />
            <Label>Number of close Words</Label>
            <Input
                type="range"
                name="range"
                id="pos1"
                min={2}
                max={30}
                step={1}
                bind:value={numCloseWords}
                placeholder="Range placeholder"
            />
            <Label>Number of far Words</Label>
            <Input
                type="range"
                name="range"
                id="neg1"
                min={0}
                max={30}
                step={1}
                bind:value={numFarWords}
                placeholder="Range placeholder"
            />
        {/if}
    </div>
    <FormGroup>
        <Input
            type="text"
            bind:value={checkIfExistsString2}
            valid={checkIfExistsValue2}
            invalid={!checkIfExistsValue2}
            feedback={checkIfExistsValue2
                ? "Embedding exists"
                : "Embedding does not exist"}
        />
        {#if checkIfExistsValue}
            <img
                src={provider.getTSNEPlotURL(
                    preprocessString(checkIfExistsString2),
                    numCloseWords2,
                    numFarWords2
                )}
                alt="plot"
                style="width: 27em; height: 27em"
            />
            <br />
            <Label>Number of close Words</Label>
            <Input
                type="range"
                name="range"
                id="pos1"
                min={2}
                max={30}
                step={1}
                bind:value={numCloseWords2}
                placeholder="Range placeholder"
            />
            <Label>Number of far Words</Label>
            <Input
                type="range"
                name="range"
                id="neg1"
                min={0}
                max={30}
                step={1}
                bind:value={numFarWords2}
                placeholder="Range placeholder"
            />
        {/if}
    </FormGroup>
</div>
<Form>
    <FormGroup>
        <h4>Doesn't match</h4>
        <Input
            type="text"
            bind:value={doesntMatchString}
            feedback={doesntMatchValue + " does not match"}
            invalid={true}
        />
    </FormGroup>
</Form>
<h4>x is to y like z is to...</h4>
<Form inline>
    <Input type="text" bind:value={x1} valid={x1IsValid} invalid={!x1IsValid} />
    <Label style="margin: 5px">is to</Label>
    <Input type="text" bind:value={y1} valid={y1IsValid} invalid={!y1IsValid} />
    <Label style="margin: 5px">like</Label>
    <Input type="text" bind:value={x2} valid={x2IsValid} invalid={!x2IsValid} />
    <Label style="margin: 5px">is to</Label>
    <Input
        type="text"
        disabled
        bind:value={y2[0][0]}
        feedback={y2.slice(0, 3)}
        valid
    />
</Form>

<style>
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
