import Chart from "react-apexcharts";

export default function TrafficFlowLineChart() {

    const OPTIONS = {
        chart: {
            id: "basic-bar"
        },
        xaxis: {
            categories: [1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998]
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