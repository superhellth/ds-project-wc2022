<script lang="ts">
    import Tweet from "../typescript/tweet_management/tweet";
    import {Card, CardBody, CardFooter, CardHeader, CardImg, Col, Row} from "sveltestrap";

    export let data: Tweet;

    let shadow = "";

    function onOver() {
        shadow = "shadow";
    }

    function onLeave() {
        shadow = "";
    }

</script>



<div class="h-100">
    <Card color="primary" outline class="mt-4 mb-4" >
        <div on:mouseover={() => {onOver()}} class={shadow} on:mouseleave={() => {onLeave()}}>
            <CardHeader>
                <Row>
                    <Col xs="2">
                        <div>
                            <CardImg src={data.getAuthor().getProfileImageURL()} />
                        </div>
                    </Col>
                    <Col xs="10">
                        <h5>
                            {data.getAuthor().getName()} (@{data.getAuthor().getUsername()})
                        </h5>
                    </Col>
                </Row>
            </CardHeader>
            <CardBody>
                {data.getText()}
            </CardBody>
            <CardFooter>
                - {data.getAgeInHours()} minutes ago
            </CardFooter>
        </div>
    </Card>
</div>
