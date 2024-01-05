import { ApexOptions } from "apexcharts";
import Chart from "react-apexcharts";
import { PRIMARY_COLOR } from "../utils/colors";

export default function TrafficFlowLineChart() {

    const OPTIONS: ApexOptions = {
        chart: {
            id: "basic-bar"
        },
        xaxis: {
            categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
        },
        colors: [PRIMARY_COLOR],
        stroke: {
            lineCap: "round",
            curve: "smooth",
        },
    };

    const SERIES = [
        {
            name: "series-1",
            data: [30, 40, 45, 50, 49, 60, 70, 91]
        }
    ]

    return (
        <>
            <Chart
                options={OPTIONS}
                series={SERIES}
                type="line"
                height="100%"
            />
        </>
    );
}