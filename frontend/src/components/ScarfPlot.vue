<script setup lang="ts">
import apexchart from "vue3-apexcharts"
import { ref } from "vue"
// Implemented with reference to
// https://apexcharts.com/javascript-chart-demos/area-charts/spline/
const options = ref({
    stroke: {
        curve: 'smooth'
    },
    dataLabels: {
        enabled: false
    },
    xaxis: {
        type: 'datetime',
        categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
    },
    tooltip: {
        x: {
            format: 'dd/MM/yy HH:mm'
        },
    },
})

const series = ref([
    {
        name: 'series1',
        data: [31, 40, 28, 51, 42, 109, 100]
    },
    {
        name: 'series2',
        data: [11, 32, 45, 32, 34, 52, 41]
    },
    {
        name: 'series3',
        data: [11, 32, 45, 32, 34, 52, 41]
    },
    {
        name: 'series4',
        data: [11, 32, 45, 32, 34, 52, 41]
    },
    {
        name: 'series5',
        data: [11, 32, 45, 32, 34, 52, 41]
    }
])

</script>

<template>
    <div>
        <apexchart height="250" type="heatmap" :options="options" :series="series"></apexchart>
    </div>
</template>

<style scoped></style>
