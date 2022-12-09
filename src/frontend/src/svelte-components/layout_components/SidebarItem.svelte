<script>
    import {createEventDispatcher} from "svelte";
    import {Icon} from "sveltestrap";

    const dispatch = createEventDispatcher();

    export let text = "";
    export let href = "javascript:void(0)";
    export let iconName = "";

    let className = "";
    export {className as class};
    const handleClick = () => {
        dispatch("press");
    };
</script>

<a class="nav-link {className}" {href} on:click={handleClick}>
    {#if iconName !== ""}
        <div class="sb-nav-link-icon">
            <Icon name={iconName}/>
        </div>
    {/if}
    {text}
</a>
