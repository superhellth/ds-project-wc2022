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


    let currentTheme: string | null;
    function toggleTheme() {
        if (currentTheme == "light") {
            document.documentElement.setAttribute("data-theme", "dark");
            localStorage.setItem("theme", "dark");
        } else {
            document.documentElement.setAttribute("data-theme", "light");
            localStorage.setItem("theme", "light");
        }
        currentTheme = localStorage.getItem("theme")
            ? localStorage.getItem("theme")
            : null;
    }
</script>

<Navbar class="sb-topnav navbar-expand" style="background-color: var(--nav-bar-color)" dark expand="md">
    <NavbarBrand style="color: var(--primary-color)">{title}</NavbarBrand>
    <!-- TODO: Add Breadcrumbs to navigate  -->
    <!-- Adds a switch to the right side of the Navbar to toggle on dark mode -->
    <FormGroup>
        <!-- TODO: Add functionality to dark mode if we decide to use it -->
        <Input id="c3" type="switch" label="Dark mode" on:input={toggleTheme} checked/>
    </FormGroup>
</Navbar>
