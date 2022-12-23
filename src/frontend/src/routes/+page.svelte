<script lang="ts">
  import FormField from "@smui/form-field";
  import IconButton from "@smui/icon-button";
  import Switch from "@smui/switch";
  import Textfield from "@smui/textfield";
  import Layout from "../svelte-components/Layout.svelte";
  import StreamControl from "../typescript/api_connections/streamControl";

  // This gets called whenever the user clicks the image button next to the text field
  // sends rule to middleware and resets the text inside the text field
  async function onSendRule() {
    rulePromise = streamControl.setRule(typedRule);
    typedRule = "";
  }

  // Toggles query
  async function onToggleQuery() {
    let isRunning = await isRunningPromise;
    if (isRunning) {
      isRunning = await streamControl.stopStream();
    } else {
      isRunning = await streamControl.startStream();
    }
    isRunningPromise = streamControl.isStreamRunning();
  }

  // Our connection to the middleware
  const streamControl: StreamControl = StreamControl.getInstance();

  // We get the stream rule, stream status and a list of the 50 most recent tweets asynchronosly,
  // thus the data type is Promise
  let rulePromise: Promise<string> = streamControl.getRule();
  let isRunningPromise: Promise<boolean> = streamControl.isStreamRunning();

  // This variable keeps track of the string in the rule textfield
  let typedRule: string = "";
</script>

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

  <title>Settings - Stream</title>
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

<style>
  .query-management {
    margin: 2em;
  }

  body {
    margin: 0;
  }
</style>
