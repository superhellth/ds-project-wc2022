<script lang="ts">
    // Adds a NavigationBar on top of the webpage
    import Navbar from "sveltestrap/src/Navbar.svelte";
    import NavbarBrand from "sveltestrap/src/NavbarBrand.svelte";

    import {FormGroup, Input} from "sveltestrap";

    export let color;
    export let title;
</script>

<Navbar class="sb-topnav navbar-expand" {color} dark expand="md">
    <NavbarBrand>{title}</NavbarBrand>
    <!-- TODO: Add Breadcrumbs to navigate  -->
    <!-- Adds a switch to the right side of the Navbar to toggle on dark mode -->
    <FormGroup>
        <!-- TODO: Add functionality to dark mode if we decide to use it -->
        <Input id="c3" type="switch" label="Dark mode"/>
    </FormGroup>
</Navbar>
