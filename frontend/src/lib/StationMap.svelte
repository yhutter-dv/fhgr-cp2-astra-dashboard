<script>
    import L from "leaflet";
    import "leaflet-tilelayer-swiss";
    import { onMount } from "svelte";
    import { CANTON_COLOR_MAP, SELECTED_COLOR } from "../utils/colors";
    import { ICON_MAP } from "../utils/icons";
    import { createEventDispatcher } from "svelte";

    export let stations = [];

    export let numberOfErrorsPerCanton = [];
    $: {
        // Remove all markers
        stationsLayer.clearLayers();
        stations.forEach((station) => {
            // Add number of errors per canton as property -> Look it up via the canton property of the station itself
            const matches = numberOfErrorsPerCanton.filter(
                (e) => e.canton === station.canton,
            );
            if (matches.length > 0) {
                station.numberOfErrorsForCanton = matches[0].numberOfErrors;
            } else {
                // Here we assume that no errors are there otherwise we would have had a match
                station.numberOfErrorsForCanton = 0;
            }
            const marker = createStationMarker(station);
            stationsLayer.addLayer(marker);
        });
    }

    const dispatch = createEventDispatcher();

    let stationsLayer = L.layerGroup();
    let leafletLayerControl = null;
    let leafletMap = null;
    let lastSelectedMarker = null;
    let selectedMarker = null;
    let selectedStation = null;
    $: {
        dispatch("selectedStationChanged", {
            selected: selectedStation,
        });
    }
    let markerSelected = false;

    function setupMap() {
        // Create map and attach id to element with id "mapid"
        const map = L.map("map", {
            // Use LV95 (EPSG:2056) projection
            crs: L.CRS.EPSG2056,
        });

        // Create layer control and add layers for measurement stations
        const layerControl = L.control.layers();
        layerControl.addOverlay(stationsLayer, "Measurement Stations");
        layerControl.addTo(map);

        // Enable stations layer
        stationsLayer.addTo(map);

        // Add Swiss layer with default options
        // @ts-ignore
        map.addLayer(L.tileLayer.swiss());

        // Center the map on Switzerland
        map.fitSwitzerland();
        return { map, layerControl };
    }

    function createMarkerIcon(station, isSelected = false) {
        // Depending on the number of errors we show a different icon and modify the color
        const icon =
            station.numberOfErrors === 0 ? ICON_MAP.check : ICON_MAP.error;
        const color = CANTON_COLOR_MAP[station.canton];
        const markerIcon = L.divIcon({
            className: isSelected ? SELECTED_COLOR : color,
            html: isSelected ? icon.selected : icon.default,
        });
        return markerIcon;
    }

    function createStationMarker(station) {
        const eastCoordinate = station.eastLv95;
        const northCoordinate = station.northLv95;
        const popup = L.popup().setContent(
            `<p><b>${station.name}</b></p><p>Errors: ${station.numberOfErrors} out of ${station.numberOfErrorsForCanton} errors total for canton ${station.canton}</p>`,
        );

        const markerIcon = createMarkerIcon(station);
        const marker = L.marker(
            L.CRS.EPSG2056.unproject(L.point(eastCoordinate, northCoordinate)),
            { icon: markerIcon },
        ).bindPopup(popup);
        marker.station = station;
        marker.on("click", onMarkerClicked);
        return marker;
    }

    function onMarkerClicked(event) {
        lastSelectedMarker = selectedMarker;
        selectedMarker = event.target;
        if (selectedMarker.station.id === lastSelectedMarker?.station?.id) {
            // User has clicked on the same marker therefore toggle the selection state
            markerSelected = !markerSelected;
        } else {
            // Different marker has been selected then previous one therefore set it as selected and deselect the previous marker
            markerSelected = true;
            const markerIcon = createMarkerIcon(selectedMarker.station, false);
            lastSelectedMarker?.setIcon(markerIcon);
        }
        // Set the selection state of the current marker
        const markerIcon = createMarkerIcon(
            selectedMarker.station,
            markerSelected,
        );
        selectedMarker.setIcon(markerIcon);
        // Read back station which is associated with the marker.
        selectedStation = markerSelected ? selectedMarker.station : null;
    }

    onMount(() => {
        const { map, layerControl } = setupMap();
        leafletMap = map;
        leafletLayerControl = layerControl;
    });
</script>

<div class="z-30" id="map" style="width: 100%; height: 100%;"></div>
