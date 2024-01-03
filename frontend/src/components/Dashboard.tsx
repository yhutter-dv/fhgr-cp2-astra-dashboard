import { Tab } from "@headlessui/react";
import { FilterSettings } from "../models/FilterSettings";
import FilterSideBar from "./FilterSidebar";
import HeatmapChart from "./HeatmapChart";
import StationMap from "./StationMap";
import TrafficFlowLineChart from "./TrafficFlowLineChart";
import TrafficSpeedLineChart from "./TrafficSpeedLineChart";
import { useState } from "react";
import { Station } from "../models/Station";

export default function Dashboard() {

  function onApplyFilterSettings(settings: FilterSettings) {
    console.log("Received the following filter settings", settings);
  }

  const [station, setStations] = useState<Array<Station>>([]);

  return (
    <div>
      <FilterSideBar onApplyFilterSettings={onApplyFilterSettings} />
      <div className="relative left-0 top-32 px-4 pl-64">
        <div className="grid grid-cols-1 xl:grid-cols-2 grid-flow-row  gap-4 px-4 ">

          {/* Station Map */}
          <div className="bg-white rounded-md shadow-md p-4">
            <div className="flex flex-row justify-between">
              <h1 className="font-bold text-lg py-2">Map</h1>
            </div>

            <div className="h-96">
              <StationMap stations={[]} />
            </div>
          </div>

          <div className="bg-white rounded-md shadow-md p-4">
            <div className="flex flex-row justify-between">
              <h1 className="font-bold text-lg py-2">Traffic Flow</h1>
            </div>

            <div className="h-96">
              <TrafficFlowLineChart />
            </div>

          </div>

          <div className="bg-white rounded-md shadow-md p-4">
            <div className="flex flex-row justify-between">
              <h1 className="font-bold text-lg py-2">Heatmap</h1>
            </div>

            <Tab.Group>
              <Tab.List className="flex justify-end space-x-4 p-1">
                <Tab className="bg-white py-1 px-4 shadow-md font-medium rounded hover:bg-blue-600 hover:text-white transition ease-in border border-sky-600">Error</Tab>
                <Tab className="bg-white py-1 px-4 shadow-md font-medium rounded hover:bg-blue-600 hover:text-white transition ease-in border border-sky-600">Traffic Flow</Tab>
                <Tab className="bg-white py-1 px-4 shadow-md font-medium rounded hover:bg-blue-600 hover:text-white transition ease-in border border-sky-600">Traffic Speed</Tab>
              </Tab.List>
              <Tab.Panels>
                <Tab.Panel>
                  <div className="h-96">
                    <HeatmapChart />
                  </div>
                </Tab.Panel>
                <Tab.Panel>
                  <div className="h-96">
                    <HeatmapChart />
                  </div>
                </Tab.Panel>
                <Tab.Panel>
                  <div className="h-96">
                    <HeatmapChart />
                  </div>
                </Tab.Panel>
              </Tab.Panels>
            </Tab.Group>



          </div>

          <div className="bg-white rounded-md shadow-md p-4">
            <div className="flex flex-row justify-between">
              <h1 className="font-bold text-lg py-2">Traffic Speed</h1>
            </div>

            <div className="h-96">
              <TrafficSpeedLineChart />
            </div>

          </div>

        </div>

      </div>
    </div>
  )
}