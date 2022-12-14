<script lang="ts">
  import FormField from "@smui/form-field";
  import IconButton from "@smui/icon-button";
  import LayoutGrid, { Cell } from "@smui/layout-grid";
  import Switch from "@smui/switch";
  import Textfield from "@smui/textfield";
  import ElasticHelper from "../typescript/api_connections/elasticonnection";
  import TweetComp from "../svelte-components/TweetComp.svelte";
  import type Tweet from "../typescript/tweet_management/tweet";
  import Layout from "../svelte-components/Layout.svelte";

  // This gets called whenever the user clicks the image button next to the text field
  // sends rule to middleware and resets the text inside the text field
  async function onSendRule() {
    rulePromise = elasticHelper.setRule(typedRule);
    typedRule = "";
  }

  // Toggles query
  async function onToggleQuery() {
    let isRunning = await isRunningPromise;
    if (isRunning) {
      isRunning = await elasticHelper.stopStream();
    } else {
      isRunning = await elasticHelper.startStream();
    }
    isRunningPromise = elasticHelper.isStreamRunning();
  }

  // Our connection to the middleware
  const elasticHelper: ElasticHelper = new ElasticHelper();

  // We get the stream rule, stream status and a list of the 50 most recent tweets asynchronosly,
  // thus the data type is Promise
  let rulePromise: Promise<string> = elasticHelper.getRule();
  let isRunningPromise: Promise<boolean> = elasticHelper.isStreamRunning();
  const tweets: Promise<Array<Tweet>> = elasticHelper.getTweets();

  // This variable keeps track of the string in the rule textfield
  let typedRule: string = "";
</script>

<Layout>

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
        <p style="clear: left">
          Current rule: {rule == null ? "invalid" : rule}
        </p>
      {/await}
    </FormField>
  </div>
</Layout>

<style>
  .query-management {
    margin: 2em;
  }

  body {
    margin: 0;
  }
</style>
