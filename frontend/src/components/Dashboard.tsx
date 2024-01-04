import { FilterSettings } from "../models/FilterSettings";
import FilterSideBar from "./FilterSidebar";
import HeatmapChart from "./HeatmapChart";
import StationMap from "./StationMap";
import TrafficFlowLineChart from "./TrafficFlowLineChart";
import TrafficSpeedLineChart from "./TrafficSpeedLineChart";
import { useState } from "react";
import { Station } from "../models/Station";
import { Button, Card, CardBody, Typography } from "@material-tailwind/react";

export default function Dashboard() {

  function onApplyFilterSettings(settings: FilterSettings) {
    console.log("Received the following filter settings", settings);
  }

  const [station, setStations] = useState<Array<Station>>([]);

  return (
    <div>
      <FilterSideBar onApplyFilterSettings={onApplyFilterSettings} />
      <div className="relative left-0 top-0 pt-6  px-4 pl-64">
        <div className="grid grid-cols-1 xl:grid-cols-2 grid-flow-row  gap-4 px-4 ">

          <Card>
            <CardBody >
              <Typography variant="h5" color="blue-gray" className="mb-2">
                Station Map
              </Typography>
              <div className="h-96">
                <StationMap stations={[]} />

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
    </div>
  )
}