<script lang="ts">
    import Drawer, {Content, Header, Subtitle, Title} from "@smui/drawer";
    import List, { Item, Text, Graphic, Separator, Subheader } from '@smui/list';
    export let open = false;
</script>

<body>
    <Drawer variant="modal" fixed={true} bind:open>
        <Header>
            <Title>Navigation</Title>
            <Subtitle>blablabla</Subtitle>
        </Header>
        <Content>
            <List>
                <Item href="/">
                    <Graphic class="material-icons" aria-hidden="true">home</Graphic>
                    <Text>Home</Text>
                </Item>
                <Item href="/tweet-overview">
                    <Graphic class="material-icons" aria-hidden="true">inbox</Graphic>
                    <Text>Tweets</Text>
                </Item>
                <Item href="/tweet-overview">
                    <Graphic class="material-icons" aria-hidden="true">check</Graphic>
                    <Text>Results</Text>
                </Item>
            </List>
        </Content>
    </Drawer>
</body>