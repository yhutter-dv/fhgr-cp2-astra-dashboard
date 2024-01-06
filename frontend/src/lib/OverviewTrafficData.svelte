<script>
    import ApexCharts from "apexcharts";
    import { onMount } from "svelte";

    function generateData(numberOfElements, config) {
        let data = [];
        const difference = config.max - config.min;
        for (let i = 0; i < numberOfElements; i++) {
            const value = Math.round(difference * Math.random()) + config.min;
            data.push(value);
        }
        return data;
    }

    // Implemented with reference to: https://apexcharts.com/javascript-chart-demos/heatmap-charts/basic/
    const OPTIONS = {
        series: [
            {
                name: "Metric1",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric2",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric3",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric4",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric5",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric6",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric7",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric8",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
            {
                name: "Metric9",
                data: generateData(18, {
                    min: 0,
                    max: 90,
                }),
            },
        ],
        chart: {
            height: 350,
            type: "heatmap",
        },
        dataLabels: {
            enabled: false,
        },
        colors: ["#008FFB"],
        title: {
            text: "HeatMap Chart (Single color)",
        },
    };

    onMount(() => {
        var chart = new ApexCharts(
            document.getElementById("overview-traffic-data"),
            OPTIONS,
        );
        chart.render();
    });
</script>

<div id="overview-traffic-data"></div>
