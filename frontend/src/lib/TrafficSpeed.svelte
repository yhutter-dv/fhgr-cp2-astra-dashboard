<script>
    import ApexCharts from "apexcharts";
    import { onMount } from "svelte";

    // Implemented with reference to: https://apexcharts.com/javascript-chart-demos/area-charts/spline/
    const OPTIONS = {
        series: [
            {
                name: "series1",
                data: [31, 40, 28, 51, 42, 109, 100],
            },
            {
                name: "series2",
                data: [11, 32, 45, 32, 34, 52, 41],
            },
        ],
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
            categories: [
                "2018-09-19T00:00:00.000Z",
                "2018-09-19T01:30:00.000Z",
                "2018-09-19T02:30:00.000Z",
                "2018-09-19T03:30:00.000Z",
                "2018-09-19T04:30:00.000Z",
                "2018-09-19T05:30:00.000Z",
                "2018-09-19T06:30:00.000Z",
            ],
        },
        tooltip: {
            x: {
                format: "dd/MM/yy HH:mm",
            },
        },
    };

    onMount(() => {
        var chart = new ApexCharts(
            document.getElementById("traffic-speed-chart"),
            OPTIONS,
        );
        chart.render();
    });
</script>

<div class="bg-white p-4 rounded shadow-lg">
    <div class="flex flex-row justify-between mb-4">
        <p class="font-semibold">Traffic Speed</p>
    </div>
    <div id="traffic-speed-chart"></div>
</div>
