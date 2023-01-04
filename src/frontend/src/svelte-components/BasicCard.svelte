<script lang="ts">
    // Import Svelte components from the sveltestrap library
    import {Card, CardBody, CardFooter, CardHeader, Icon} from "sveltestrap";

    // Add header, footer text and chart_id as variables that can be passed to the component
    export let header: string;
    export let footer: string;
</script>

<!-- Create a Card using the sveltestrap library -->
<Card body color="dark" inverse>
    <!-- The Card has a header, which displays the text passed to the "header" variable and a Twitter icon -->
    <CardHeader>
        <div>{header} <Icon name="twitter"/></div>
    </CardHeader>
    <!-- The "card-header-controls" slot allows additional content to be added to the header of the Card -->
    <CardHeader>
        <slot name="card-header-controls"/>
    </CardHeader>
    <!-- The Card body contains a canvas element with the specified "chart_id" -->
    <CardBody>
        <slot name="body"/>
    </CardBody>
    <!-- The Card footer displays the text passed to the "footer" variable -->
    <CardFooter>
        {footer}
    </CardFooter>
</Card>