<script lang="ts">
    // Import Svelte components used in this script
    import {
        Breadcrumb,
        BreadcrumbItem,
    } from "sveltestrap";
    import {fly} from "svelte/transition";
</script>

<title>Overview - Tweets</title>
<h1>Tweet Query</h1>
<Breadcrumb class="mb-4">
    <BreadcrumbItem>
        <a href=".">Dashboard</a>
    </BreadcrumbItem>
    <BreadcrumbItem active>Scrap Yard</BreadcrumbItem>
</Breadcrumb>

<div in:fly={{ x: 400, duration: 400, delay: 200 }}>
    <h4>Idea 1</h4>
    <p>
        This did not work because...
    </p>
    <h4>Idea 2</h4>
    <p>
        This did not work because...
    </p>
</div>
