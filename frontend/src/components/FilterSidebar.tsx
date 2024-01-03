import { Switch } from '@headlessui/react';
import { useEffect, useState } from 'react';
import ListBox from './ListBox';
import { FilterSettings } from '../models/FilterSettings';

type Props = {
    onApplyFilterSettings: (filterSettings: FilterSettings) => void
}

export default function FilterSideBar({ onApplyFilterSettings }: Props) {

    const API_BASE_URL = import.meta.env.VITE_API_URL;

    const timeRanges = [
        "4h",
        "8h",
        "2d",
    ];

    const directions = [
        "positive",
        "negative",
    ];

    const vehicleTypes = [
        "car",
        "lorry",
        "anyVehicle",
    ];

    async function fetchCantons() {
        console.log("Fetching cantons...");
        const response = await fetch(`${API_BASE_URL}/cantons`);
        if (response.ok) {
            const result = await response.json() as Array<string>;
            setCantons([...result]);
            setSelectedCanton(cantons[0]);
        } else {
            console.warn("Failed to fetch Cantons...");
        }
    }

    function publishFilterSettings() {
        const settings: FilterSettings = {
            canton: selectedCanton,
            timeRange: selectedTimeRange,
            direction: selectedDirection,
            vehicleType: selectedVehicleType
        };
        onApplyFilterSettings(settings);
    }

    const [cantons, setCantons] = useState<Array<string>>(["No Canton selected"]);
    const [selectedCanton, setSelectedCanton] = useState<string>(cantons[0]);

    const [selectedTimeRange, setSelectedTimeRange] = useState<string>(timeRanges[0]);
    const [selectedDirection, setSelectedDirection] = useState<string>(directions[0]);
    const [selectedVehicleType, setSelectedVehicleType] = useState<string>(vehicleTypes[0]);

    const [liveModeEnabled, setLiveModeEnabled] = useState<boolean>(true);

    useEffect(() => {
        fetchCantons();
    }, []);

    return (
        <div className="fixed top-0 left-0 z-40 w-64 pt-32 px-4 h-screen bg-white border border-r-1">
            <div className="flex flex-col justify-start">
                <div className='flex flex-row justify-start items-center mb-4'>
                    <Switch
                        checked={liveModeEnabled}
                        onChange={setLiveModeEnabled}
                        className={`${liveModeEnabled ? 'bg-blue-600' : 'bg-gray-200'
                            } relative inline-flex h-6 w-11 items-center rounded-full mr-2`}
                    >
                        <span className="sr-only">Toggle Filter Sidebar</span>
                        <span
                            className={`${liveModeEnabled ? 'translate-x-6' : 'translate-x-1'
                                } inline-block h-4 w-4 transform rounded-full bg-white transition`}
                        />
                    </Switch>
                    <h1 className='text-sm font-medium'>Live Update</h1>
                </div>

                <div className="my-6">
                    <p className='mb-4 font-bold'>Canton</p>
                    <ListBox selectedElement={selectedCanton} elements={cantons} onSelectedElementChanged={setSelectedCanton} />
                </div>

                <div className="my-6">
                    <p className='mb-4 font-bold'>Time Range</p>
                    <ListBox selectedElement={selectedTimeRange} elements={timeRanges} onSelectedElementChanged={setSelectedTimeRange} />
                </div>

                <div className="my-6">
                    <p className='mb-4 font-bold'>Direction</p>
                    <ListBox selectedElement={selectedDirection} elements={directions} onSelectedElementChanged={setSelectedDirection} />
                </div>

                <div className="my-6">
                    <p className='mb-4 font-bold'>Vehicle Type</p>
                    <ListBox selectedElement={selectedVehicleType} elements={vehicleTypes} onSelectedElementChanged={setSelectedVehicleType} />
                </div>

                <div className='my-8'>
                    <button
                        type="button"
                        onClick={publishFilterSettings}
                        className="w-full rounded-md bg-blue-500 px-4 py-2 text-sm font-medium text-white hover:bg-blue-600 focus:outline-none focus-visible:ring-2 focus-visible:ring-offset-blue-300"
                    >
                        Apply Filter
                    </button>
                </div>



            </div>
        </div>


    );
}