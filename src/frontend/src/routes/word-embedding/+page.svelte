<script lang="ts">
    import Loading from "src/svelte-components/Loading.svelte";
    import TweetCard from "src/svelte-components/TweetCard.svelte";
    import MiddlewareProvider from "src/typescript/api_connections/middlewareConnection";
    import { onMount } from "svelte";
    import { fly } from "svelte/transition";
    import {
        Breadcrumb,
        BreadcrumbItem,
        Form,
        FormGroup,
        Input,
        Label,
        Image,
        Progress,
        Col,
        Row,
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

    let visible: boolean = false;

    onMount(async () => {
        visible = true;
    });

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

    let transDuration: number = 400;
</script>

<title>Text Analytics - Word2Vec</title>

<h1>Word2Vec Embedding</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Word2Vec</BreadcrumbItem>
</Breadcrumb>

{#if visible}
    <h3 in:fly={{ y: 400, duration: transDuration, delay: 0 }}>
        Explore the Embedding
    </h3>
    <p in:fly={{ y: 400, duration: transDuration, delay: transDuration / 2 }}>
        Our Embedding is a gensim Word2Vec Model trained on our whole corpus.
        The training parameters have been finetuned to fit out corpus. Our
        dataset is big enough, that things like "Hansi Flick" - "Germany" +
        "France" = "Didier Deschamps" work. However our data is very football
        specific, so "King" - "Man" + "Woman" does not work quite as well.
    </p>
    <h4 in:fly={{ y: 400, duration: transDuration, delay: transDuration }}>
        Check for Embedding
    </h4>
{/if}
{#if checkIfExistsValue && checkIfExistsValue2}
    {#await provider.getDistance(preprocessString(checkIfExistsString), preprocessString(checkIfExistsString2)) then distance}
        <div
            style="margin: 1em"
            in:fly={{
                y: 400,
                duration: transDuration,
                delay: 0,
            }}
        >
            <p style="margin: auto; width: 50%; text-align: center">
                Distance between Words: {distance}
            </p>
            <Progress
                value={100 - distance * 100}
                style="margin: auto; width: 50%;"
            />
        </div>
    {/await}
    <div
        style="display: flex; justify-content: space-evenly"
        in:fly={{ y: 400, duration: transDuration, delay: transDuration * 2 }}
    >
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
                        numFarWords,
                        "1"
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
                        numFarWords2,
                        "2"
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
    <div in:fly={{ y: 400, duration: transDuration, delay: transDuration * 3 }}>
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
    </div>
    <div in:fly={{ y: 400, duration: transDuration, delay: transDuration * 4 }}>
        <h4>x is to y like z is to...</h4>
        <Form inline>
            <Input
                type="text"
                bind:value={x1}
                valid={x1IsValid}
                invalid={!x1IsValid}
            />
            <Label style="margin: 5px">is to</Label>
            <Input
                type="text"
                bind:value={y1}
                valid={y1IsValid}
                invalid={!y1IsValid}
            />
            <Label style="margin: 5px">like</Label>
            <Input
                type="text"
                bind:value={x2}
                valid={x2IsValid}
                invalid={!x2IsValid}
            />
            <Label style="margin: 5px">is to</Label>
            <Input
                type="text"
                disabled
                bind:value={y2[0][0]}
                feedback={y2.slice(0, 3)}
                valid
            />
        </Form>
    </div>

    <div in:fly={{ y: 400, duration: transDuration, delay: transDuration * 5}}>
        <h3>Results</h3>
        <p>
            First of all it should be noted, that the quality of the embedding
            is quite good. There is a lot of football knowledge encoded here.
            The embedding "knows" the players of the popular teams and roughly
            which teams were in which group. Apart from that the embedding helps
            getting a better overview about the topics discovered in the Word
            and Entity Graph. E. g. Looking up the nft embedding shows which
            platforms have been pushed. However we can also derive some
            knowledge about the criticism on Qatar. Simply looking at the
            distance between "Human Rights" and "Qatar" (0.59) shows us, that
            these two Phrases are connected. The distance is normed so that 0
            means the phrases are the same and values >=1 mean that the phrases
            are not connected at all. But now how large of a distance is 0.59?
            "Kane" and "England" have a distance of 0.58. "Messi" and "Ronaldo":
            0.18. "Qatar" and "Host Nation": 0.39. So 0.59 definitely indicates
            a familiarity, however not a too close one. Furthermore let's just
            look at the close words of "Human Rights".
        </p>
        <img src="human rights-tsne.png" style="width: 27em; height: 27em" />
        <p>
            There we can see many obvious neighbors like "Rights Abuses" and
            "Migrant Workers" which shows that criticsim on the host nations
            does exist. But why are there also phrases like "Hypocrisy",
            "Western countries" and "Condemning". Taking a look at the Tweets
            containing these phrases we can see that there actually is quite
            some criticism against western countries condemning the Qatari
            sportswashing.
        </p>
        <Row>
            {#each [1594350868870168576n, 1606283271431749632n, 1594686111485501441n, 1594302492866711552n] as id}
                {#await provider.getTweetByID(id)}
                    <Loading displayString="Tweet" />
                {:then tweet}
                    <Col>
                        <TweetCard
                            data={tweet}
                            showDetails={false}
                            sentimentMethod="None"
                            sentimentScore={0}
                            sentimentMethodIndex={-1}
                        />
                    </Col>
                {/await}
            {/each}
        </Row>

        <p>
            So it seems like the FIFA and Qatar did manage to present the World
            Cup in such a way that some people see Qatar more as a victim than
            an offender.
        </p>
    </div>
{/if}

<style>
    img {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
