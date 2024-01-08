<script>
    import ApexCharts from "apexcharts";
    import { onDestroy, onMount } from "svelte";
    import { CHART_PRIMARY_COLOR } from "../utils/colors";
    import { numberOfErrorsPerCantonMeasurements } from "../stores/dashboardStore";
    import Overlay from "./Overlay.svelte";

    let apexChart = null;
    let numberOfErrorsPerCantonMeasurementsSubscription = null;
    let numberOfErrorsPerCantonMeasurementsData = [];
    let overlayText = "No Data";
    let showOverlay = true;

    // Implemented with reference to: https://apexcharts.com/javascript-chart-demos/heatmap-charts/basic/
    const OPTIONS = {
        series: [],
        chart: {
            height: 350,
            type: "heatmap",
        },
        dataLabels: {
            enabled: false,
        },
        colors: [CHART_PRIMARY_COLOR],
        plotOptions: {
            heatmap: {
                radius: 2,
            },
        },
    };

    function updateData() {
        if (apexChart === null) {
            console.warn("Apex Chart reference is still null...");
            return;
        }
        const newSeries = numberOfErrorsPerCantonMeasurementsData.map((m) => {
            return {
                name: m.name,
                data: m.measurements.map((e) => {
                    return {
                        x: e.time,
                        y: e.numberOfErrors,
                    };
                }),
            };
        });
        apexChart.updateSeries(newSeries);
    }

    function updateOverlay() {
        const hasData =
            numberOfErrorsPerCantonMeasurementsData.length > 0 &&
            numberOfErrorsPerCantonMeasurementsData.some(
                (d) => d.measurements.length > 0,
            );
        showOverlay = hasData === false;
        if (hasData === false) {
            overlayText = "No Data found...";
        }
    }

    onMount(() => {
        apexChart = new ApexCharts(
            document.getElementById("overview-traffic-data"),
            OPTIONS,
        );
        apexChart.render();

        numberOfErrorsPerCantonMeasurementsSubscription =
            numberOfErrorsPerCantonMeasurements.subscribe((data) => {
                numberOfErrorsPerCantonMeasurementsData = data;
                updateData();
                updateOverlay();
            });
    });

    onDestroy(() => {
        numberOfErrorsPerCantonMeasurementsSubscription();
    });
</script>

<div class="bg-white p-4 rounded shadow-lg">
    <div class="flex flex-row justify-between mb-4">
        <p class="font-semibold">Overview Number Of Errors</p>
    </div>
    <div class="relative">
        <div id="overview-traffic-data"></div>
        {#if showOverlay}
            <Overlay text={overlayText} />
        {/if}
    </div>
</div>
