<script>
  import { onMount } from "svelte";
  import StationMap from "./lib/StationMap.svelte";
  import { DEFAULT_FILTER_SETTINGS } from "./utils/filterValues";
  import Header from "./lib/Header.svelte";
  import FilterSidebar from "./lib/FilterSidebar.svelte";
  import TrafficFlow from "./lib/TrafficFlow.svelte";
  import TrafficSpeed from "./lib/TrafficSpeed.svelte";
  import OverviewTrafficData from "./lib/OverviewTrafficData.svelte";

  let cantons = [];
  let stations = [];
  let numberOfErrorsPerCanton = [];
  let selectedStation = null;
  let filterSettings = DEFAULT_FILTER_SETTINGS;

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  onMount(() => {
    getCantons();
    getNumberOfErrorsForCantons();
    getStations();
  });

  function onApplyFilter(settings) {
    filterSettings = { ...settings };
    getStations();
  }

  function selectedStationChanged(station) {
    selectedStation = station;
  }

  async function getCantons() {
    const response = await fetch(`${API_BASE_URL}/cantons`);
    const result = await response.json();
    cantons = [...result];
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
      <div class="bg-white p-1 rounded shadow-lg">
        <div class="h-96">
          <StationMap
            {stations}
            {numberOfErrorsPerCanton}
            on:selectedStationChanged={(e) =>
              selectedStationChanged(e.detail.selected)}
          />
        </div>
      </div>

      <div class="bg-white p-1 rounded shadow-lg">
        <TrafficFlow />
      </div>

      <div class="bg-white p-1 rounded shadow-lg">
        <TrafficSpeed />
      </div>

      <div class="bg-white p-1 rounded shadow-lg">
        <OverviewTrafficData />
      </div>
    </div>
  </div>
</main>
