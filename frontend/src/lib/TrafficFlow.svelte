<script>
    import ApexCharts from "apexcharts";
    import { onDestroy, onMount } from "svelte";
    import Overlay from "./Overlay.svelte";
    import { trafficFlowMeasurements } from "../stores/dashboardStore";

    export let showOverlay = false;
    export let overlayText = "";

    let apexChart = null;
    let trafficFlowSubscription = null;

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

    function updateData(data) {
        console.log(apexChart);
        if (apexChart === null) {
            console.warn("Apex Chart reference is still null...");
            return;
        }
        const newSeries = data.map((m) => {
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
        console.log("Created new instance of apex chart ref...");
        apexChart.render();

        trafficFlowSubscription = trafficFlowMeasurements.subscribe((data) => {
            updateData(data);
        });
    });

    onDestroy(trafficFlowSubscription);
</script>

<div class="relative">
    <div id="traffic-flow-chart"></div>
    {#if showOverlay}
        <Overlay text={overlayText} />
    {/if}
</div>
