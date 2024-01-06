<script>
  import { onMount } from "svelte";
  import StationMap from "./lib/StationMap.svelte";
  import { DEFAULT_FILTER_SETTINGS } from "./utils/filterValues";
  import Header from "./lib/Header.svelte";
  import FilterSidebar from "./lib/FilterSidebar.svelte";
  import TrafficFlow from "./lib/TrafficFlow.svelte";
  import TrafficSpeed from "./lib/TrafficSpeed.svelte";
  import OverviewTrafficData from "./lib/OverviewTrafficData.svelte";
  import { trafficFlowMeasurements } from "./stores/dashboardStore";
  import { get } from "svelte/store";

  let cantons = [];
  let stations = [];
  let numberOfErrorsPerCanton = [];
  let selectedStation = null;
  let filterSettings = DEFAULT_FILTER_SETTINGS;

  let trafficFlowOverlayText = "Please choose at least one Station on the Map.";
  let showTrafficFlowOverlay = true;

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  onMount(async () => {
    await getCantons();
    await getNumberOfErrorsForCantons();
    await getStations();
    updateOverlays();
  });

  function getDetectorsWithIndexAccordingToFilterValues(measurementType) {
    // First get the detectors with the matching direction
    const detectorsWithValidDirection = selectedStation.detectors.filter(
      (d) => d.direction === filterSettings.direction,
    );

    // Next filter by vehicle type and measurement and get out corresponding indices
    const detectorsWithIndex = detectorsWithValidDirection.map((d) => {
      const validCharacteristics = d.characteristics.filter(
        (c) =>
          c.measurement === measurementType &&
          c.vehicleType === filterSettings.vehicleType,
      );
      const validIndices = validCharacteristics.map((c) => c.index);
      if (validIndices.length > 1) {
        console.warn("Got more then one index...");
      }
      // In case of an error the index must be zero
      const index = selectedStation.numberOfErrors > 0 ? 0 : validIndices[0];
      return {
        id: d.id,
        index: index,
      };
    });
    return detectorsWithIndex;
  }

  function updateOverlays() {
    const flowData = get(trafficFlowMeasurements);
    const hasData =
      flowData.length > 0 && flowData.some((d) => d.measurements.length > 0);
    console.log("Has Data is", hasData);
    showTrafficFlowOverlay = selectedStation === null || hasData === false;
    if (selectedStation === null) {
      trafficFlowOverlayText = "Please choose at least one Station on the Map.";
    } else if (hasData === false) {
      trafficFlowOverlayText = "No Data found...";
    }
  }

  async function onApplyFilter(settings) {
    filterSettings = { ...settings };
    getStations();
    const detectorsWithIndex =
      getDetectorsWithIndexAccordingToFilterValues("trafficFlow");
    await getDetectorMeasurements(detectorsWithIndex);
    updateOverlays();
  }

  function selectedStationChanged(station) {
    selectedStation = station;
  }

  async function getCantons() {
    const response = await fetch(`${API_BASE_URL}/cantons`);
    const result = await response.json();
    cantons = [...result];
  }

  async function getDetectorMeasurements(detectorsWithIndex) {
    const body = JSON.stringify({
      detectorMeasurements: detectorsWithIndex,
      time: filterSettings.timeRange,
    });
    const response = await fetch(`${API_BASE_URL}/detector_measurements`, {
      method: "POST",
      body: body,
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    });
    const result = await response.json();
    trafficFlowMeasurements.set([...result]);
  }

  async function getStations() {
    const body = {
      canton: filterSettings.canton,
      time: filterSettings.timeRange,
    };
    const response = await fetch(`${API_BASE_URL}/stations`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    });
    const result = await response.json();
    stations = [...result];
  }

  async function getNumberOfErrorsForCantons() {
    const body = {
      canton: filterSettings.canton,
      time: filterSettings.timeRange,
    };
    const response = await fetch(`${API_BASE_URL}/cantons/numberOfErrors`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    });
    const result = await response.json();
    numberOfErrorsPerCanton = [...result];
  }
</script>

<main>
  <Header />
  <FilterSidebar
    {cantons}
    on:applyFilter={(e) => onApplyFilter(e.detail.settings)}
  />

  <!-- Dashboard Content -->
  <div class="relative left-0 top-32 px-4 pl-64">
    <div class="grid grid-cols-1 xl:grid-cols-2 grid-flow-row gap-4 px-4">
      <!-- Station Map (needs defined height, e.g h-96) -->
      <div class="bg-white p-4 rounded shadow-lg">
        <div class="flex flex-row justify-between mb-4">
          <p class="font-semibold">Station Map</p>
        </div>
        <div class="h-96">
          <StationMap
            {stations}
            {numberOfErrorsPerCanton}
            on:selectedStationChanged={(e) =>
              selectedStationChanged(e.detail.selected)}
          />
        </div>
      </div>

      <div class="bg-white p-4 rounded shadow-lg">
        <div class="flex flex-row justify-between mb-4">
          <p class="font-semibold">Traffic Flow</p>
        </div>
        <TrafficFlow
          showOverlay={showTrafficFlowOverlay}
          overlayText={trafficFlowOverlayText}
        />
      </div>

      <div class="bg-white p-4 rounded shadow-lg">
        <div class="flex flex-row justify-between mb-4">
          <p class="font-semibold">Traffic Speed</p>
        </div>
        <TrafficSpeed />
      </div>

      <div class="bg-white p-4 rounded shadow-lg">
        <div class="flex flex-row justify-between mb-4">
          <p class="font-semibold">Overview Traffic Data</p>
        </div>
        <OverviewTrafficData />
      </div>
    </div>
  </div>
</main>
