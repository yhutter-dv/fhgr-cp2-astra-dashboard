// Global variables
const apiBaseUrl = "http://localhost:8000";

// Global Leaflet layers
let stationsLayer = L.layerGroup();

function setupMap () {
    // Create map and attach id to element with id "mapid"
    const map = L.map('map', {
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
    map.addLayer(L.tileLayer.swiss());

    // Center the map on Switzerland
    map.fitSwitzerland();
    return { map, layerControl };
}

function createStationMarker(station) {
    const eastCoordinate = station.eastLv95;
    const northCoordinate = station.northLv95;
    const name = station.name;
    return L.marker(L.CRS.EPSG2056.unproject(L.point(eastCoordinate, northCoordinate))).bindPopup(name);
}


async function fetchStations(canton = "") {
    const response = await fetch(`${apiBaseUrl}/mst?canton=${canton}`);
    const stations = await response.json();
    return stations;
}

async function fetchCantons() {
    const response = await fetch(`${apiBaseUrl}/cantons`);
    const cantons = await response.json();
    return cantons;
}

async function cantonsDropDownChanged(selectedCanton, map, layerControl) {
    // Remove all markers
    stationsLayer.clearLayers();
    // Fetch all stations and create a marker on the map for the selected canton.
    const stations = await fetchStations(selectedCanton);
    stations.forEach(station => {
        const marker = createStationMarker(station);
        stationsLayer.addLayer(marker);
    });
}

async function onLoad() {
    const { map, layerControl } = setupMap();

    // Populate cantons dropdown
    const cantons = await fetchCantons();
    const cantonsDropDown = document.getElementById("canton-select");
    cantons.forEach(canton => {
        const cantonOption = document.createElement("option");
        cantonOption.textContent = canton;
        cantonOption.value = canton;
        cantonsDropDown.appendChild(cantonOption);
    });

    // Add Event Listener for Change
    cantonsDropDown.addEventListener("change", (event) => cantonsDropDownChanged(event.target.value, map, layerControl));

    // Trigger inital change manually so 
    cantonsDropDownChanged("", map, layerControl);
}

window.addEventListener("load", onLoad)