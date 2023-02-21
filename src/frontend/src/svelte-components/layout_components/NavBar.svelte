<script lang="ts">
    // Import the Navbar and NavbarBrand components from the svelte-strap library
    import Navbar from "sveltestrap/src/Navbar.svelte";
    import NavbarBrand from "sveltestrap/src/NavbarBrand.svelte";

    // Import the FormGroup and Input components from the svelte-strap library
    import { Button, FormGroup, Icon, Input, NavbarToggler } from "sveltestrap";

    // Define a variable for the title of the NavbarBrand
    export let title: string;

    export let sideBarIsOpen: boolean = true;

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

<Navbar
    class="sb-topnav navbar-expand"
    style="background-color: var(--nav-bar-color)"
    dark
    expand="md"
>
    <Button style="background: transparent; border: 0" on:click={() => sideBarIsOpen = !sideBarIsOpen}
        ><Icon name="list" /></Button
    >
    <NavbarBrand style="color: var(--primary-color)">{title}</NavbarBrand>
    <FormGroup>
        <Input
            id="c3"
            type="switch"
            label="Dark mode"
            on:input={toggleTheme}
            checked
        />
    </FormGroup>
</Navbar>
