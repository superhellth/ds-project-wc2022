<script lang="ts">
    // Import custom Svelte components for the layout
    import Footer from "src/svelte-components/layout_components/Footer.svelte";
    import NavBar from "src/svelte-components/layout_components/NavBar.svelte";
    import SideBar from "src/svelte-components/layout_components/SideBar.svelte";

    // Import Svelte components from the sveltestrap library
    import {Container} from "sveltestrap";

    // Declare variables that can be passed to the layout
    export let color = "dark";
    export let title = "Dashboard - 2022 World Cup on Twitter";

    let sideBarIsOpen: boolean = true;
</script>

<body>
<!-- The layout includes a fixed navigation bar and a fluid main content area -->
<div class="sb-nav-fixed">
    <!-- Use the NavBar component to create the navigation bar, passing the "color" and "title" variables to customize it -->
    <NavBar {title} bind:sideBarIsOpen/>
    <div id="layoutSidenav">
        <!-- Use the SideBar component to create the sidebar, passing the "color" variable to customize it -->
        <SideBar theme={color} bind:isOpen={sideBarIsOpen}/>
        <div
                id="layoutSidenav_content"
                style="background-color: var(--background-color);"
        >
            <main>
                <!-- Use the Container component from sveltestrap to create a fluid container for the main content of the page -->
                <Container fluid={true}>
                    <!-- Use the slot element to insert the content of other pages into the layout -->
                    <slot/>
                </Container>
            </main>
            <!-- Use the Footer component to create the footer, passing the "color" variable to customize it -->
            <Footer {color}/>
        </div>
    </div>
</div>
</body>

<style lang="scss">
  @use "src/themes";

  main {
    margin: 3px;
  }

  body {
    background-color: white;
  }
</style>
