<script lang="ts">
    import Tweet from "../typescript/tweet_management/tweet";
    import {Card, CardBody, CardFooter, CardHeader, CardImg} from "sveltestrap";

    export let data: Tweet;
</script>

<div>
    <Card class="mt-4 mb-4">
        <CardHeader>
            <h5>
                {data.getAuthor().getName()} (@{data.getAuthor().getUsername()})
            </h5>
        </CardHeader>
        <CardBody>
            {data.getText()}
<!--            TODO: Insert image nicely-->
<!--            <CardImg src={data.getAuthor().getProfileImageURL()}/>-->
        </CardBody>
        <CardFooter>
            - {data.getAgeInHours()} minutes ago
        </CardFooter>
    </Card>
</div>
