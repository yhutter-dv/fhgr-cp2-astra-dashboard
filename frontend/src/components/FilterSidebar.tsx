import { useEffect, useState } from 'react';
import { FilterSettings } from '../models/FilterSettings';
import { Card, Typography, Input, Select, Option, Button, Switch } from '@material-tailwind/react';

type Props = {
    onApplyFilterSettings: (filterSettings: FilterSettings) => void
}

// Implemented with reference to 
// - https://www.material-tailwind.com/docs/react/sidebar
// - https://www.material-tailwind.com/docs/react/select

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
    const [selectedCanton, setSelectedCanton] = useState<string | undefined>(cantons[0]);

    const [selectedTimeRange, setSelectedTimeRange] = useState<string | undefined>(timeRanges[0]);
    const [selectedDirection, setSelectedDirection] = useState<string | undefined>(directions[0]);
    const [selectedVehicleType, setSelectedVehicleType] = useState<string | undefined>(vehicleTypes[0]);


    useEffect(() => {
        // fetchCantons();
    }, []);

    return (
        <Card className="fixed top-0 z-40 pt-32 w-full max-w-[16rem] rounded-none left-0 h-screen shadow-xl shadow-blue-gray-900/5">
            <div className='flex flex-col justify-start px-8'>
                <div className="mb-12">
                    <Typography variant="h5" color="blue-gray">
                        Filter Settings
                    </Typography>
                </div>

                <div className="mb-1 flex flex-col gap-12">
                    <Select variant="outlined" label="Select Canton" value={selectedCanton} onChange={setSelectedCanton}>
                        {
                            cantons.map(c => (<Option value={c} key={c}>{c}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Time" value={selectedTimeRange} onChange={setSelectedTimeRange}>
                        {
                            timeRanges.map(t => (<Option value={t} key={t}>{t}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Vehicle Type" value={selectedVehicleType} onChange={setSelectedVehicleType}>
                        {
                            vehicleTypes.map(v => (<Option value={v} key={v}>{v}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Direction" value={selectedDirection} onChange={setSelectedDirection}>
                        {
                            directions.map(d => (<Option value={d} key={d}>{d}</Option>))
                        }
                    </Select>

                    <Button className="mt-6" fullWidth onClick={publishFilterSettings}>
                        Apply Filter
                    </Button>

                </div>
            </div>


        </Card>
    );
}