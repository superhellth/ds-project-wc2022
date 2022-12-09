<script lang="ts">
    // This layout file is used as a 'base' for all other pages.
    // It contains the NavigationBar, the Sidebar and the Footer
    // Content of pages has to be inside '<Layout>' if the layout should be used

    import {Container} from "sveltestrap";
    import NavBar from "./layout_components/NavBar.svelte";
    import Footer from "./layout_components/Footer.svelte";
    import SideBar from "./layout_components/SideBar.svelte";

    export let color = "dark";
    export let title = "Dashboard - 2022 World Cup on Twitter";

</script>

<div class="sb-nav-fixed">
    <NavBar {color} {title}/>
    <div id="layoutSidenav">
        <SideBar theme={color}/>
        <div id="layoutSidenav_content">
            <main>
                <Container fluid={true}>
                    <slot/>
                </Container>
            </main>
            <Footer {color}/>
        </div>
    </div>
</div>
