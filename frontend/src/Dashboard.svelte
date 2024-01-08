<script>
  import { onMount } from "svelte";
  import StationMap from "./lib/StationMap.svelte";
  import { DEFAULT_FILTER_SETTINGS } from "./utils/filterValues";
  import Header from "./lib/Header.svelte";
  import FilterSidebar from "./lib/FilterSidebar.svelte";
  import TrafficFlow from "./lib/TrafficFlow.svelte";
  import TrafficSpeed from "./lib/TrafficSpeed.svelte";
  import OverviewTrafficData from "./lib/OverviewTrafficData.svelte";
  import {
    trafficFlowMeasurements,
    stationsWithTotalNumberOfErrorsPerCanton,
    cantons,
    selectedStation,
    trafficSpeedMeasurements,
    numberOfErrorsPerCantonMeasurements,
  } from "./stores/dashboardStore";
  import { get } from "svelte/store";

  let filterSettings = DEFAULT_FILTER_SETTINGS;

  const API_BASE_URL = import.meta.env.VITE_API_URL;

  onMount(async () => {
    const cantonsResult = await getCantons();
    cantons.set([...cantonsResult]);
    stationsWithTotalNumberOfErrorsPerCanton.set(
      await getStationsWithTotalNumberOfErrorsPerCanton(),
    );
    numberOfErrorsPerCantonMeasurements.set(await getNumberOfErrorsPerCanton());
  });

  function getDetectors(measurementType, station, vehicleType, direction) {
    // First get the detectors with the matching direction
    const detectorsWithValidDirection = station.detectors.filter(
      (d) => d.direction === direction,
    );

    // Next filter by vehicle type and measurement and get out corresponding indices
    const detectorsWithIndex = detectorsWithValidDirection.map((d) => {
      const validCharacteristics = d.characteristics.filter(
        (c) =>
          c.measurement === measurementType && c.vehicleType === vehicleType,
      );
      const validIndices = validCharacteristics.map((c) => c.index);
      if (validIndices.length > 1) {
        console.warn("Got more then one index...");
      }
      // In case of an error the index must be zero
      const index = station.numberOfErrors > 0 ? 0 : validIndices[0];
      return {
        id: d.id,
        index: index,
        name: d.name,
      };
    });
    return detectorsWithIndex;
  }

  async function onApplyFilter(settings) {
    filterSettings = { ...settings };

    // Clear measurement data...
    trafficFlowMeasurements.set([]);
    trafficSpeedMeasurements.set([]);
    numberOfErrorsPerCantonMeasurements.set([]);

    stationsWithTotalNumberOfErrorsPerCanton.set(
      await getStationsWithTotalNumberOfErrorsPerCanton(),
    );

    numberOfErrorsPerCantonMeasurements.set(await getNumberOfErrorsPerCanton());

    // Only try get data if a station is selected.
    const station = get(selectedStation);
    if (station === null) {
      console.warn(
        "No stations is selected, will no try getting traffic flow and speed data...",
      );
      return;
    }
    const trafficFlowDetectors = getDetectors(
      "trafficFlow",
      station,
      filterSettings.vehicleType,
      filterSettings.direction,
    );
    const trafficFlow = await getDetectorMeasurements(trafficFlowDetectors);
    trafficFlowMeasurements.set(trafficFlow);

    const trafficSpeedDetectors = getDetectors(
      "trafficSpeed",
      station,
      filterSettings.vehicleType,
      filterSettings.direction,
    );
    const trafficSpeed = await getDetectorMeasurements(trafficSpeedDetectors);
    trafficSpeedMeasurements.set(trafficSpeed);
  }

  function selectedStationChanged(station) {
    selectedStation.set(station);
  }

  async function getCantons() {
    const response = await fetch(`${API_BASE_URL}/cantons`);
    const result = await response.json();
    return result;
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
    return result;
  }

  async function getStationsWithTotalNumberOfErrorsPerCanton() {
    const stations = await getStations();
    const totalNumberOfErrorsPerCanton =
      await getTotalNumberOfErrorsForCantons();
    const result = {
      stations: stations,
      totalNumberOfErrorsPerCanton: totalNumberOfErrorsPerCanton,
    };
    return result;
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
    return result;
  }

  async function getTotalNumberOfErrorsForCantons() {
    const body = {
      canton: filterSettings.canton,
      time: filterSettings.timeRange,
    };
    const response = await fetch(
      `${API_BASE_URL}/cantons/total_number_of_errors`,
      {
        method: "POST",
        body: JSON.stringify(body),
        headers: {
          "Content-type": "application/json; charset=UTF-8",
        },
      },
    );
    const result = await response.json();
    return result;
  }

  async function getNumberOfErrorsPerCanton() {
    // TODO: Find out good bin size for each Time Range
    const body = {
      canton: filterSettings.canton,
      time: filterSettings.timeRange,
      binSize: "5s",
    };
    const response = await fetch(`${API_BASE_URL}/cantons/number_of_errors`, {
      method: "POST",
      body: JSON.stringify(body),
      headers: {
        "Content-type": "application/json; charset=UTF-8",
      },
    });
    const result = await response.json();
    return result;
  }
</script>

<main>
  <Header />
  <FilterSidebar on:applyFilter={(e) => onApplyFilter(e.detail.settings)} />

  <!-- Dashboard Content -->
  <div class="relative left-0 top-32 px-4 pl-64">
    <div class="grid grid-cols-1 xl:grid-cols-2 grid-flow-row gap-4 px-4">
      <StationMap
        on:selectedStationChanged={(e) =>
          selectedStationChanged(e.detail.selected)}
      />

      <TrafficFlow />

      <OverviewTrafficData />

      <TrafficSpeed />
    </div>
  </div>
</main>
