import Toastify from 'toastify-js';
import Chart from 'chart.js/auto';
import 'chartjs-adapter-dayjs-4/dist/chartjs-adapter-dayjs-4.esm';

// Global variables
const apiBaseUrl = "http://localhost:8000";
const defaultMarkerColor = "#4a86cf";
const selectedMarkerColor = "#1a5fb4";
const updateIntervalMs = 1000;

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
let selectedCanton = null;

// Charts

let lineChartForTrafficFlow = null;
let lineChartForTrafficFlowUpdateInteralId = null;
let lineChartTrafficFlowLiveUpdateEnabled = false;

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

    // TODO: Depending on the number of errors we change the marker color
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
        // User has clicked on the same marker therefore toggle the selection state
        markerSelected = !markerSelected;
    } else {
        // Different marker has been selected then previous one therefore set it as selected and deselect the previous marker
        markerSelected = true;
        lastSelectedMarker?.setIcon(defaultMarkerIcon);
    }
    // Set the selection state of the current marker
    const icon = markerSelected === true ? selectedMarkerIcon : defaultMarkerIcon;
    selectedMarker.setIcon(icon)
    // Read back station which is associated with the customData property.
    selectedStation = markerSelected ? selectedMarker.customData : null;
}

function validateFilterValues() {
    const noFilterValueNull = selectedStation !== null && selectedVehicleType !== null && selectedDirection !== null && selectedTimeRange !== null;
    const noFilterValueEmpty = selectedStation !== "" && selectedVehicleType !== "" && selectedDirection !== "" && selectedTimeRange !== "";
    return noFilterValueNull && noFilterValueEmpty;
}

function showToast(message) {
    Toastify({
        text: message,
        className: "toast-message",
        gravity: "bottom",
        position: "center"
    }).showToast();
}

function getDetectorsWithIndexAccordingToFilterValues(measurementType) {
    // First get the detectors with the matching direction
    const detectorsWithValidDirection = selectedStation.detectors.filter(d => d.direction === selectedDirection);

    // Next filter by vehicle type and measurement and get out corresponding indices
    const detectorsWithIndex = detectorsWithValidDirection.map(d => {
        const validCharacteristics = d.characteristics.filter(c => c.measurement === measurementType && c.vehicleType === selectedVehicleType);
        const validIndices = validCharacteristics.map(c => c.index);
        if (validIndices.length > 1) {
            console.warn("Got more then one index...");
        }
        return {
            id: d.id,
            index: validIndices[0],
        };
    });
    return detectorsWithIndex;
}

async function onApplyFilterClicked(event) {
    if (!validateFilterValues()) {
        showToast("Please make sure that you have a Station, Direction, Vehicle Type and Time Range selected...")
        return;
    }
    const detectorsWithIndex = getDetectorsWithIndexAccordingToFilterValues("trafficFlow");
    const detectorMeasurements = await getDetectorMeasurements(detectorsWithIndex);
    updateLineChartForTrafficFlow(detectorMeasurements);
}

async function getDetectorMeasurements(detectorsWithIndex) {
    const body = JSON.stringify({
        "detectorMeasurements": detectorsWithIndex,
        "time": selectedTimeRange
    });
    const response = await fetch(`${apiBaseUrl}/detector_measurements`, {
        method: "POST",
        body: body,
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    const detectorMeasurements = await response.json();
    return detectorMeasurements;
}


async function getStations(canton = "") {
    const body = {
        "canton": canton,
        "time": selectedTimeRange
    };
    const response = await fetch(`${apiBaseUrl}/stations`, {
        method: "POST",
        body: JSON.stringify(body),
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

async function getNumberOfErrorsForCantons() {
    const body = {
        "canton": selectedCanton,
        "time": selectedTimeRange
    };
    const response = await fetch(`${apiBaseUrl}/cantons/numberOfErrors`, {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
    const numberOfErrorsPerCanton = await response.json();
    console.log(numberOfErrorsPerCanton);
    return numberOfErrorsPerCanton;
}

async function onCantonsDropDownChanged(canton, map, layerControl) {
    // Remove all markers
    stationsLayer.clearLayers();
    selectedStation = null;
    selectedCanton = canton;
    const numberOfErrorsPerCanton = await getNumberOfErrorsForCantons();
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


function updateLineChartForTrafficFlow(detectorMeasurements) {
    // Create a new series for each detector measurement
    const dataSets = detectorMeasurements.map((detector) => {
        return {
            label: detector.id,
            data: detector.measurements.map((measurement) => {
                return {
                    x: measurement.time,
                    y: measurement.value
                }
            })
        }
    });
    lineChartForTrafficFlow.data.datasets = dataSets;
    lineChartForTrafficFlow.update();
}

function liveUpdateLineChartForTrafficFlow() {
    console.log("Live Updating line chart for traffic flow");
    lineChartForTrafficFlow.data.datasets.forEach(d => {
        // TODO: Call endpoint periodically to fetch data...
        const newData = {
            x: new Date(),
            y: Math.random() * 10
        }
        d.data.push(newData);
    });
    lineChartForTrafficFlow.update();
}

function createLineChartForTrafficFlow() {
    const context = document.getElementById("line-chart-for-traffic-flow");
    const config = {
        type: 'line',
        bounds: 'data',
        options: {
            scales: {
                x: {
                    type: "time",
                }
            },
            responsive: true
        },
    };
    const chart = new Chart(context, config);
    return chart;
}

function toggleLiveUpdateForLineChartTrafficFlow(enabled) {
    lineChartTrafficFlowLiveUpdateEnabled = enabled;
    if (lineChartTrafficFlowLiveUpdateEnabled) {
        lineChartForTrafficFlowUpdateInteralId = setInterval(liveUpdateLineChartForTrafficFlow, updateIntervalMs);
    } else {
        clearInterval(lineChartForTrafficFlowUpdateInteralId );
    }
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
    const checkboxLiveModeLineChartForTrafficFlow = document.getElementById("checkbox-live-mode-line-chart-traffic-flow");
    const applyFilterButton = document.getElementById("apply-filter-button");

    lineChartForTrafficFlow = createLineChartForTrafficFlow();

    // Add Event Listeners
    cantonsDropDown.addEventListener("change", (event) => onCantonsDropDownChanged(event.target.value, map, layerControl));
    directionDropDown.addEventListener("change", (event) => onDirectionDropDownChanged(event.target.value));
    timeRangeDropDown.addEventListener("change", (event) => onTimeRangeDropDownChanged(event.target.value));
    vehicleTypeDropDown.addEventListener("change", (event) => onVehicleTypeDropDownChanged(event.target.value));
    checkboxLiveModeLineChartForTrafficFlow.addEventListener("change", (event) => toggleLiveUpdateForLineChartTrafficFlow(event.target.checked));
    applyFilterButton.addEventListener("click", onApplyFilterClicked);

    checkboxLiveModeLineChartForTrafficFlow.checked = lineChartTrafficFlowLiveUpdateEnabled;
    toggleLiveUpdateForLineChartTrafficFlow(checkboxLiveModeLineChartForTrafficFlow.checked);

    // Trigger inital change manually so the map gets updated properly 
    onCantonsDropDownChanged(cantonsDropDown.options[cantonsDropDown.selectedIndex].value, map, layerControl);
    onDirectionDropDownChanged(directionDropDown.options[directionDropDown.selectedIndex].value);
    onTimeRangeDropDownChanged(timeRangeDropDown.options[timeRangeDropDown.selectedIndex].value);
    onVehicleTypeDropDownChanged(vehicleTypeDropDown.options[vehicleTypeDropDown.selectedIndex].value);

}

window.addEventListener("load", onLoad)
