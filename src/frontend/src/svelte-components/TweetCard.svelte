<script lang="ts">
    // Import the Tweet type and the Card component from the sveltestrap library
    import Tweet from "../typescript/tweet_management/tweet";
    import {Card, CardBody, CardFooter, CardHeader, CardImg, Col, Icon, Row} from "sveltestrap";

    // Define a variable for storing the tweet data
    export let data: Tweet;

    // Define a variable for storing the shadow effect
    let shadow = "";

    // Define a function for adding the shadow effect when the mouse is over the element
    function onOver() {
        shadow = "shadow";
    }

    // Define a function for removing the shadow effect when the mouse is no longer over the element
    function onLeave() {
        shadow = "";
    }
</script>



<div class="h-100">
    <Card color="dark" outline class="mt-4 mb-4" >
        <!-- Add a class to the div, which will be used to apply the hover effect -->
        <div on:mouseover={() => {onOver()}} class="{shadow} bg-tweet hover-effect" on:mouseleave={() => {onLeave()}}>
            <CardHeader>
                <!-- Use a row and columns to lay out the elements in the header -->
                <Row>
                    <Col xs="2">
                        <!-- Wrap the image in a div to properly size it -->
                        <div>
                            <CardImg src={data.getAuthor().getProfileImageURL()} />
                        </div>
                    </Col>
                    <Col xs="10">
                        <!-- Use the name and username of the author to create a link to their twitter profile -->
                        <h5>
                            {data.getAuthor().getName()} (<a href="https://www.twitter.com/{data.getAuthor().getUsername()}">@{data.getAuthor().getUsername()}</a>)
                        </h5>
                    </Col>
                </Row>
            </CardHeader>
            <!-- Use the text method to get the text of the tweet -->
            <CardBody>
                {data.getText()}
            </CardBody>
            <CardFooter>
                <!-- Use an icon to indicate that this is a tweet, and the ageInHours method to show how long ago it was posted -->
                <Icon name="twitter"/> {data.getAgeInHours()}
            </CardFooter>
        </div>
    </Card>
</div>
