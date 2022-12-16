<script lang="ts">
    // Import the Navbar and NavbarBrand components from the svelte-strap library
    import Navbar from "sveltestrap/src/Navbar.svelte";
    import NavbarBrand from "sveltestrap/src/NavbarBrand.svelte";

    // Import the FormGroup and Input components from the svelte-strap library
    import {FormGroup, Input} from "sveltestrap";

    // Define a variable for the color of the Navbar
    export let color: any;

    // Define a variable for the title of the NavbarBrand
    export let title: string;
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
