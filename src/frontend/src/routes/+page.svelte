<script lang="ts">
    import { onMount } from "svelte";
    import { fly, fade, slide } from "svelte/transition";
    import ElasticProvider from "src/typescript/api_connections/elasticProvider";
    import { Icon } from "sveltestrap";

    let provider: ElasticProvider = ElasticProvider.getInstance();
    let visible: boolean = false;
    let map: any;

    async function createMap() {
        let L = await import("leaflet");
        map = L.map("map", {
            center: [0, 0],
            zoom: 2,
        });

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            attribution:
                'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>',
            maxZoom: 10,
            minZoom: 1,
        }).addTo(map);

        let locations: Map<string, number> = await provider.getTermHistogram(
            "author.location",
            50
        );
        for (const [key, value] of locations) {
            let locationPos = await getCoordinates(key);
            if (locationPos.lat == 0 && locationPos.lng == 0) {
                continue;
            }
            let marker = L.circle([locationPos.lat, locationPos.lng], {
                color: "red",
                fillColor: "#f03",
                fillOpacity: 0.5,
                radius: Math.min(value * 10, 200000),
            }).addTo(map);
            marker.bindPopup("<b>" + key + "</b><br>" + value + " Tweets")
            await new Promise((r) => setTimeout(r, 1100));
        }
    }

    async function getCoordinates(location: string) {
        const response = await fetch(
            `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(
                location
            )}&format=json`
        );
        const data = await response.json();

        if (data.length > 0) {
            return {
                lat: data[0].lat,
                lng: data[0].lon,
            };
        } else {
            return {
                lat: 0,
                lng: 0,
            };
        }
    }

    onMount(async () => {
        visible = true;
        createMap();
    });
</script>

<!-- <h1>Exploring the perception of the 2022 FIFA World Cup</h1> -->
{#if visible}
    <div in:fly={{ y: 200, duration: 2000 }} out:fade>
        <img src="Qatar-2022-1536x798.png" class="banner" />
        <p style="margin-left: 80em; font-size: 0.8em">
            <Icon name="exclamation-circle" /> Copyright by
        </p>
    </div>
    <div
        style="display: flex; justify-content: center"
        in:fly={{ y: 200, duration: 2000, delay: 0 }}
        out:fade
    >
        <p>
            We collected <span class="highlight">5.025.511</span> Tweets from
            <span class="highlight">1.521.959</span>
            different users over the course of
            <span class="highlight">54</span> days.
        </p>
    </div>
    <p style="color: white">von fiete errechnet (im kopf sogar)</p>
    <div
        style="display: flex; justify-content: center"
        in:fly={{ y: -200, duration: 2000 }}
        out:fade
    >
        <div id="map" />
    </div>
{/if}

<style lang="scss">
    @use "src/themes";

    #map {
        height: 900px;
        width: 1200px;
    }
    p {
        font-size: 1.2em;
    }
    .banner {
        width: 100%;
        height: 300px;
        object-fit: scale-down;
        margin-top: 3em;
        margin-bottom: 3em;
    }
    .highlight {
        font-size: 2em;
        background-color: var(--qatar-color);
        color: white;
    }
</style>
