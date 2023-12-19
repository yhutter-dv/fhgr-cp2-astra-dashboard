import Toastify from 'toastify-js';

// Global variables
const apiBaseUrl = "http://localhost:8000";
const defaultMarkerColor = "#4a86cf";
const selectedMarkerColor = "#1a5fb4";

const selectedMarkerIcon = L.ExtraMarkers.icon({
    icon: 'bi-geo-fill',
    markerColor: selectedMarkerColor,
    shape: 'circle',
    prefix: 'bi',
    svg: true
});


const defaultMarkerIcon = L.ExtraMarkers.icon({
    icon: 'bi-geo-fill',
    markerColor: defaultMarkerColor,
    shape: 'circle',
    prefix: 'bi',
    svg: true
});

let lastSelectedMarker = null;
let selectedMarker = null;
let selectedStation = null;
let markerSelected = false;
let selectedDirection = null;
let selectedTimeRange = null;
let selectedVehicleType = null;

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
    const icon = L.ExtraMarkers.icon({
        icon: 'bi-geo-fill',
        markerColor: defaultMarkerColor,
        shape: 'circle',
        prefix: 'bi',
        svg: true
    });
    const marker = L.marker(L.CRS.EPSG2056.unproject(L.point(eastCoordinate, northCoordinate)), { icon }).bindPopup(name);
    marker.customData = station;
    marker.on("click", onMarkerClicked);
    return marker;
}


function onMarkerClicked(event) {
    lastSelectedMarker = selectedMarker;
    selectedMarker = event.target;
    if (selectedMarker.customData.id === lastSelectedMarker?.customData?.id) {
        // User has clicked on the same marker
        markerSelected = !markerSelected;
    } else {
        // Different marker has been selected then previous one
        markerSelected = true;
        // Deselect previous marker
        lastSelectedMarker?.setIcon(defaultMarkerIcon);
    }
    const icon = markerSelected === true ? selectedMarkerIcon : defaultMarkerIcon;
    selectedMarker.setIcon(icon)
    // Read back station which is associated with the customData property.
    selectedStation = markerSelected ? selectedMarker.customData : null;
}

function validateFilterValues() {
    return selectedStation !== null && selectedVehicleType !== null && selectedDirection !== null && selectedTimeRange !== null;
}

function showToast(message) {
    Toastify({
        text: message,
        className: "toast-message",
        gravity: "bottom",
        position: "center"
    }).showToast();
}

function onApplyFilterClicked(event) {
    if (!validateFilterValues()) {
        showToast("Please make sure that you have a Station, Direction, Vehicle Type and Time Range selected...")
        return;
    }
}


async function getStations(canton = "") {
    const response = await fetch(`${apiBaseUrl}/stations`, {
        method: "POST",
        body: JSON.stringify({
            canton
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    const stations = await response.json();
    return stations;
}

async function getCantons() {
    const response = await fetch(`${apiBaseUrl}/cantons`);
    const cantons = await response.json();
    return cantons;
}

async function onCantonsDropDownChanged(selectedCanton, map, layerControl) {
    // Remove all markers
    stationsLayer.clearLayers();
    selectedStation = null;
    // Fetch all stations and create a marker on the map for the selected canton.
    const stations = await getStations(selectedCanton);
    stations.forEach(station => {
        const marker = createStationMarker(station);
        stationsLayer.addLayer(marker);
    });
}

function onDirectionDropDownChanged(direction) {
    selectedDirection = direction;
}

function onTimeRangeDropDownChanged(timeRange) {
    selectedTimeRange = timeRange;
}

function onVehicleTypeDropDownChanged(vehicleType) {
    selectedVehicleType = vehicleType;
}

async function onLoad() {
    const { map, layerControl } = setupMap();

    // Populate cantons dropdown
    const cantons = await getCantons();
    const cantonsDropDown = document.getElementById("canton-select");
    cantons.forEach(canton => {
        const cantonOption = document.createElement("option");
        cantonOption.textContent = canton;
        cantonOption.value = canton;
        cantonsDropDown.appendChild(cantonOption);
    });

    const directionDropDown = document.getElementById("direction-select");
    const timeRangeDropDown = document.getElementById("time-select");
    const vehicleTypeDropDown = document.getElementById("vehicle-select");

    const applyFilterButton = document.getElementById("apply-filter-button");

    // Add Event Listeners
    cantonsDropDown.addEventListener("change", (event) => onCantonsDropDownChanged(event.target.value, map, layerControl));
    directionDropDown.addEventListener("change", (event) => onDirectionDropDownChanged(event.target.value));
    timeRangeDropDown.addEventListener("change", (event) => onTimeRangeDropDownChanged(event.target.value));
    vehicleTypeDropDown.addEventListener("change", (event) => onVehicleTypeDropDownChanged(event.target.value));
    
    applyFilterButton.addEventListener("click", onApplyFilterClicked);

    // Trigger inital change manually so the map gets updated properly 
    onCantonsDropDownChanged(cantonsDropDown.options[cantonsDropDown.selectedIndex].value, map, layerControl);
    onDirectionDropDownChanged(directionDropDown.options[directionDropDown.selectedIndex].value);
    onTimeRangeDropDownChanged(timeRangeDropDown.options[timeRangeDropDown.selectedIndex].value);
    onVehicleTypeDropDownChanged(vehicleTypeDropDown.options[vehicleTypeDropDown.selectedIndex].value);
}

window.addEventListener("load", onLoad)
