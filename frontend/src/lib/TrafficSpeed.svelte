<script>
    import ApexCharts from "apexcharts";
    import { onDestroy, onMount } from "svelte";
    import Overlay from "./Overlay.svelte";
    import {
        selectedStation,
        trafficSpeedMeasurements,
    } from "../stores/dashboardStore";

    let overlayText = "Please choose at least one Station on the Map.";
    let showOverlay = true;
    let title = "Traffic Speed";

    let apexChart = null;
    let trafficSpeedSubscription = null;
    let selectedStationSubscription = null;
    let trafficSpeedData = [];
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
            y: {
                formatter: function (
                    value,
                    { series, seriesIndex, dataPointIndex, w },
                ) {
                    const data =
                        w.globals.initialSeries[seriesIndex].data[
                            dataPointIndex
                        ];
                    const errorReasonText =
                        data.errorReason !== null
                            ? `Error Reason: ${data.errorReason}`
                            : "";
                    return `Traffic Speed: ${value} ${errorReasonText}`;
                },
            },
            x: {
                format: "dd/MM/yy HH:mm",
            },
        },
    };

    function updateTitle() {
        if (selectedStationData) {
            title = `Traffic Speed for ${selectedStationData.name}`;
        } else {
            title = `Traffic Speed`;
        }
    }

    function updateOverlay() {
        const hasData =
            trafficSpeedData.length > 0 &&
            trafficSpeedData.some((d) => d.measurements.length > 0);
        showOverlay = selectedStationData === null || hasData === false;
        if (selectedStationData === null) {
            overlayText = "Please choose at least one Station on the Map.";
        } else if (hasData === false) {
            overlayText = "No Data found...";
        }
    }

    function updateData() {
        if (apexChart === null) {
            console.warn("Apex Chart reference is still null...");
            return;
        }
        const newSeries = trafficSpeedData.map((m) => {
            const name = m.name !== null ? `${m.id} (${m.name})` : m.id;
            return {
                name: name,
                data: m.measurements.map((e) => {
                    return {
                        x: e.time,
                        y: e.value,
                        errorReason: e.errorReason,
                    };
                }),
            };
        });
        apexChart.updateSeries(newSeries);
    }

    onMount(() => {
        apexChart = new ApexCharts(
            document.getElementById("traffic-speed-chart"),
            OPTIONS,
        );
        apexChart.render();

        trafficSpeedSubscription = trafficSpeedMeasurements.subscribe(
            (data) => {
                trafficSpeedData = data;
                updateData();
                updateTitle();
                updateOverlay();
            },
        );

        selectedStationSubscription = selectedStation.subscribe((data) => {
            selectedStationData = data;
            updateOverlay();
        });
    });

    onDestroy(() => {
        // Unsubscribe
        trafficSpeedSubscription();
        selectedStationSubscription();
    });
</script>

<div class="bg-white p-4 rounded shadow-lg">
    <div class="flex flex-row justify-between mb-4">
        <p class="font-semibold">{title}</p>
    </div>
    <div class="relative">
        <div id="traffic-speed-chart"></div>
        {#if showOverlay}
            <Overlay text={overlayText} />
        {/if}
    </div>
</div>
