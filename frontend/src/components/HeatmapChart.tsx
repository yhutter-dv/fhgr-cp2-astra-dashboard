import { ApexOptions } from "apexcharts";
import Chart from "react-apexcharts";
import { PRIMARY_COLOR } from "../utils/colors";


export default function HeatmapChart() {

    const generateData = (numberOfValues: number, config: { min: number, max: number }): Array<number> => {
        let elements = [];
        for (let i = 0; i < numberOfValues; i++) {
            elements.push(Math.random() * config.max);
        }
        return elements;
    }

    const OPTIONS: ApexOptions = {
        chart: {
            id: "heatmap-chart"
        },
        dataLabels: {
            enabled: false
        },
        colors: [PRIMARY_COLOR],
    };

    const SERIES = [{
        name: 'Metric1',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric2',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric3',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric4',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric5',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric6',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric7',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric8',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    },
    {
        name: 'Metric9',
        data: generateData(18, {
            min: 0,
            max: 90
        })
    }
    ]

    return (

        <Chart
            options={OPTIONS}
            series={SERIES}
            type="heatmap"
            height="100%"
        />
    );
}