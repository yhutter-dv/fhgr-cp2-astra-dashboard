<script>
    import ApexCharts from "apexcharts";
    import { onDestroy, onMount } from "svelte";
    import Overlay from "./Overlay.svelte";
    import {
        trafficFlowMeasurements,
        selectedStation,
    } from "../stores/dashboardStore";

    let overlayText = "Please choose at least one Station on the Map.";
    let showOverlay = true;

    let apexChart = null;
    let trafficFlowSubscription = null;
    let selectedStationSubscription = null;
    let trafficFlowData = [];
    let selectedStationData = null;

    // Implemented with reference to: https://apexcharts.com/javascript-chart-demos/area-charts/spline/
    const OPTIONS = {
        series: [],
        chart: {
            height: 350,
            type: "area",
        },
        dataLabels: {
            enabled: false,
        },
        stroke: {
            curve: "smooth",
        },
        xaxis: {
            type: "datetime",
        },
        tooltip: {
            x: {
                format: "dd/MM/yy HH:mm",
            },
        },
    };

    function updateOverlay() {
        const hasData =
            trafficFlowData.length > 0 &&
            trafficFlowData.some((d) => d.measurements.length > 0);
        showOverlay = selectedStationData === null || hasData === false;
        if (selectedStationData === null) {
            overlayText = "Please choose at least one Station on the Map.";
        } else if (hasData === false) {
            overlayText = "No Data found...";
        }
    }

    function updateData() {
        console.log(apexChart);
        if (apexChart === null) {
            console.warn("Apex Chart reference is still null...");
            return;
        }
        const newSeries = trafficFlowData.map((m) => {
            return {
                name: m.id,
                data: m.measurements.map((e) => {
                    return { x: e.time, y: e.value };
                }),
            };
        });
        console.log("Updating data with series ", newSeries);
        apexChart.updateSeries(newSeries);
    }

    onMount(() => {
        apexChart = new ApexCharts(
            document.getElementById("traffic-flow-chart"),
            OPTIONS,
        );
        apexChart.render();

        trafficFlowSubscription = trafficFlowMeasurements.subscribe((data) => {
            trafficFlowData = data;
            updateData();
            updateOverlay();
        });

        selectedStationSubscription = selectedStation.subscribe((data) => {
            selectedStationData = data;
            updateOverlay();
        });
    });

    onDestroy(() => {
        // Unsubscribe
        trafficFlowSubscription();
        selectedStationSubscription();
    });
</script>

<div class="relative">
    <div id="traffic-flow-chart"></div>
    {#if showOverlay}
        <Overlay text={overlayText} />
    {/if}
</div>
