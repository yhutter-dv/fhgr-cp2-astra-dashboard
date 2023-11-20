<script setup lang="ts">
// Implemented with reference to:
// https://github.com/razorness/vue-maplibre-gl/blob/master/src/App.vue
// https://codesandbox.io/s/swisstopo-react-1nnup?file=/src/Map.js

import { MglMap } from 'vue-maplibre-gl'
import { LngLatLike } from 'maplibre-gl'
import { ref } from "vue"
import "maplibre-gl/dist/maplibre-gl.css"
import "vue-maplibre-gl/dist/vue-maplibre-gl.css"
const zoom = ref(8)
const mapStyle = ref("https://vectortiles.geo.admin.ch/styles/ch.swisstopo.leichte-basiskarte.vt/style.json")
const center = ref<LngLatLike>([8.55301, 47.35257])

</script>

<template>
    <div class="h-full">
        <mgl-map ref="map" :map-style="mapStyle" :zoom="zoom" :center="center">
        </mgl-map>
    </div>
</template>

<style scoped>
.h-full {
    /* Do not use full height as we need to subtract padding and margin (set in parent container) */
    height: calc(100% - 2rem);
}
</style>
