<script lang="ts">
    import Tweet from "../typescript/tweet_management/tweet";
    import {Card, CardBody, CardFooter, CardHeader, CardImg, Col, Icon, Row} from "sveltestrap";

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
    <Card color="dark" outline class="mt-4 mb-4" >
        <div on:mouseover={() => {onOver()}} class="{shadow} bg-tweet" on:mouseleave={() => {onLeave()}}>
            <CardHeader>
                <Row>
                    <Col xs="2">
                        <div>
                            <CardImg src={data.getAuthor().getProfileImageURL()} />
                        </div>
                    </Col>
                    <Col xs="10">
                        <h5>
                            {data.getAuthor().getName()} (<a href="https://www.twitter.com/{data.getAuthor().getUsername()}">@{data.getAuthor().getUsername()}</a>)
                        </h5>
                    </Col>
                </Row>
            </CardHeader>
            <CardBody>
                {data.getText()}
            </CardBody>
            <CardFooter>
                <Icon name="twitter"/> {data.getAgeInHours()} minutes ago
            </CardFooter>
        </div>
    </Card>
</div>
