<script lang="ts">
    import FormField from "@smui/form-field";
    import IconButton from "@smui/icon-button";
    import LayoutGrid, { Cell } from "@smui/layout-grid";
    import Switch from "@smui/switch";
    import Textfield from "@smui/textfield";
    import TopAppBar, { Row, Section, Title } from "@smui/top-app-bar";
    import ElasticHelper from "../api_connections/elasticonnection";
    import TweetComp from "./TweetComp.svelte";
    import type Tweet from "../tweet_management/tweet";
    import Button from "@smui/button/src/Button.svelte";
  
    const elasticHelper = new ElasticHelper();
    let rulePromise: Promise<string> = elasticHelper.getRule();
    let isRunningPromise: Promise<boolean> = elasticHelper.isStreamRunning();
    const tweets: Promise<Array<Tweet>> = elasticHelper.getTweets();
  
    let typedRule: string = "";
  
    async function onSendRule() {
      rulePromise = elasticHelper.setRule(typedRule);
      typedRule = "";
    }
  
    async function onToggleQuery() {
      let isRunning = await isRunningPromise;
      if (isRunning) {
        isRunning = await elasticHelper.stopStream();
      } else {
        isRunning = await elasticHelper.startStream();
      }
      isRunningPromise = elasticHelper.isStreamRunning();
    }
  </script>
  
  <div class="top-bar-container">
    <TopAppBar variant="static">
      <Row>
        <Section>
          <Title>Tweets</Title>
        </Section>
      </Row>
    </TopAppBar>
  </div>
  
  <div class="query-management">
    <div class="query-part" style="float: left;">
      <Textfield
        bind:value={typedRule}
        label="Set Query Rule"
        style="min-width: 30em; float: left;"
      />
      {#await isRunningPromise}
        <p>Checking Stream state...</p>
      {:then isRunning}
        <IconButton
          class="material-icons"
          disabled={isRunning}
          on:click={onSendRule}
          style="float: left;"
        >
          send
        </IconButton>
      {/await}
    </div>
  
    <div class="query-part" style="float: right; margin-left: 5em;">
      {#await isRunningPromise}
        <p style="float: left;">Checking state...</p>
      {:then isRunning}
        {#await rulePromise}
          <p>Checking rule...</p>
        {:then rule}
          <FormField>
            <Switch
              id="toggle-query-switch"
              disabled={rule == null}
              checked={isRunning}
              on:SMUISwitch:change={onToggleQuery}
            />
            <p style="float: left;">Stream is running: {isRunning}</p>
          </FormField>
        {/await}
      {/await}
    </div>
    <div style="clear: left;" />
    <FormField>
      {#await rulePromise}
      <p>fetching rule...</p>
      {:then rule}
      <p style="clear: left">Current rule: {rule == null ? "invalid" : rule}</p>
      {/await}
    </FormField>
  </div>
  
  <div class="tweet-list-container" style="float:left;">
    {#await tweets}
      <p>loading tweets...</p>
    {:then tweets}
      <LayoutGrid>
        {#each tweets as aTweet}
          <Cell>
            <TweetComp tweet={aTweet} />
          </Cell>
        {/each}
      </LayoutGrid>
    {/await}
  </div>
  
  <style>
    .query-management {
      margin: 2em;
    }
  </style>
