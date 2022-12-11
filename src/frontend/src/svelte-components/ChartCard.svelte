<script lang="ts">
    import {Card, CardBody, CardFooter, CardHeader, Icon} from "sveltestrap";

    // Add header, footer text
    export let header, footer, chart_id = "";
</script>


<Card>
    <CardHeader>
        <div>{header} <Icon name="twitter"/></div>
    </CardHeader>
    <CardHeader>
        <slot name="card-header-controls"/>
    </CardHeader>
    <CardBody>
        <div>
            <canvas id={chart_id}></canvas>
        </div>
    </CardBody>
    <CardFooter>
        {footer}
    </CardFooter>
</Card>
