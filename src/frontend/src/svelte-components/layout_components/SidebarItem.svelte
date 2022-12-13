<script>
    // Import the createEventDispatcher and Icon components from the svelte and svelte-strap libraries, respectively
    import {createEventDispatcher} from "svelte";
    import {Icon} from "sveltestrap";

    // Create an event dispatcher for handling custom events
    const dispatch = createEventDispatcher();

    // Define a variable for the text of the link
    export let text = "";

    // Define a variable for the href of the link
    export let href = "javascript:void(0)";

    // Define a variable for the name of the icon to be used
    export let iconName = "";

    // Define a variable for the class name of the link
    let className = "";

    // Export the className variable as "class"
    export {className as class};

    // Define a function for handling click events on the link
    const handleClick = () => {
        // Dispatch a custom "press" event when the link is clicked
        dispatch("press");
    };
</script>

<!-- Create a link with the specified text, href, and class name -->
<a class="nav-link {className}" {href} on:click={handleClick}>
    <!-- If an icon name is specified, add the icon to the link using the svelte-strap Icon component -->
    {#if iconName !== ""}
        <div class="sb-nav-link-icon">
            <Icon name={iconName}/>
        </div>
    {/if}
    {text}
</a>
