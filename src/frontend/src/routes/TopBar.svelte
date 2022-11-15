<script lang="ts">
    import TopAppBar, { Row, Section } from "@smui/top-app-bar";
    import Button, { Label } from "@smui/button";
</script>

<div class="top-bar-container">
    <TopAppBar>
        <Row>
            <Section>
                <h1>Tweets</h1>
            </Section>
        </Row>
        <Row>
            <Section>
                <Button>Tweets</Button>
                <Button>Stats</Button>
            </Section>
        </Row>
    </TopAppBar>
</div>
