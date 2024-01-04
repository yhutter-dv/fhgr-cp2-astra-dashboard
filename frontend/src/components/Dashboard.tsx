import { FilterSettings } from "../models/FilterSettings";
import FilterSideBar from "./FilterSidebar";
import HeatmapChart from "./HeatmapChart";
import StationMap from "./StationMap";
import TrafficFlowLineChart from "./TrafficFlowLineChart";
import TrafficSpeedLineChart from "./TrafficSpeedLineChart";
import { useEffect, useState } from "react";
import { Station } from "../models/Station";
import { Button, Card, CardBody, Typography } from "@material-tailwind/react";
import Header from "./Header";

export default function Dashboard() {

  const TIME_RANGES: Array<{ label: string, value: string }> = [
    {
      label: "Last 4 hours",
      value: "-4h"
    },
    {
      label: "Last 8 hours",
      value: "-8h"
    },
    {
      label: "Last Day",
      value: "-1d"
    },
    {
      label: "Last Week",
      value: "-7d"
    }
  ];

  const DIRECTIONS: Array<{ label: string, value: string }> = [
    {
      label: "Positive",
      value: "positive"
    },
    {
      label: "Negative",
      value: "negative"
    },
  ];

  const VEHICLE_TYPES: Array<{ label: string, value: string }> = [
    {
      label: "Car",
      value: "car"
    },
    {
      label: "Lorry",
      value: "lorry"
    },
    {
      label: "Any Vehicle",
      value: "anyVehicle"
    },
  ];

  const STATIONS: Array<Station> = [
    {
      latitude: 47.36667,
      longitude: 8.55,
      name: "Zürich",
      numberOfErrors: 0
    },
    {
      latitude: 46.947456,
      longitude: 7.451123,
      name: "Bern",
      numberOfErrors: 10
    }
  ];

  const API_BASE_URL = import.meta.env.VITE_API_URL;


  async function fetchCantons() {
    console.log("Fetching cantons...");
    const response = await fetch(`${API_BASE_URL}/cantons`);
    if (response.ok) {
      const result = await response.json() as Array<string>;
      setCantons([...result]);
    } else {
      console.warn("Failed to fetch Cantons...");
    }
  }

  function onApplyFilterSettings(settings: FilterSettings) {
    console.log("Received the following filter settings", settings);
  }

  function onLiveModeChanged(liveModeEnabled: boolean) {
    console.log("Live mode was set to: ", liveModeEnabled);
  }

  const [cantons, setCantons] = useState<Array<string>>(["No Canton selected"]);
  const [stations, setStations] = useState<Array<Station>>([]);

  useEffect(() => {
    // fetchCantons();
    setStations([...STATIONS]);
  }, []);


  return (
    <>
      <Header onLiveModeChanged={onLiveModeChanged} />
      <FilterSideBar cantons={cantons} timeRanges={TIME_RANGES} directions={DIRECTIONS} vehicleTypes={VEHICLE_TYPES} onApplyFilterSettings={onApplyFilterSettings} />
      <div className="relative left-0 top-0 pt-6  px-4 pl-64">
        <div className="grid grid-cols-1 xl:grid-cols-2 grid-flow-row  gap-4 px-4 ">

          <Card>
            <CardBody >
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Station Map
              </Typography>
              <div className="h-96">
                <StationMap stations={stations} />
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardBody >
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Traffic Flow
              </Typography>
              <div className="h-96">
                <TrafficFlowLineChart />
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardBody >
              <Typography variant="h5" color="blue-gray" className="mb-2">
                <div className="flex flex-row justify-between">
                  Scarfplot
                  <div className="flex flex-row gap-4">
                    <Button variant="outlined" size="sm">Error</Button>
                    <Button variant="outlined" size="sm">Traffic Flow</Button>
                    <Button variant="outlined" size="sm">Traffic Speed</Button>
                  </div>

                </div>
              </Typography>
              <div className="h-96">
                <HeatmapChart />
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardBody >
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Traffic Speed
              </Typography>
              <div className="h-96">
                <TrafficSpeedLineChart />
              </div>
            </CardBody>
          </Card>


        </div>
      </div>
    </>
  )
}