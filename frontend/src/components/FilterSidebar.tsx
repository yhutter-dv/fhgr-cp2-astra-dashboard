import { useEffect, useState } from 'react';
import { FilterSettings } from '../models/FilterSettings';
import { Card, Typography, Input, Select, Option, Button, Switch } from '@material-tailwind/react';

type Props = {
    onApplyFilterSettings: (filterSettings: FilterSettings) => void,
    cantons: Array<string>
    timeRanges: Array<{ label: string, value: string }>
    directions: Array<{ label: string, value: string }>
    vehicleTypes: Array<{ label: string, value: string }>
}

// Implemented with reference to 
// - https://www.material-tailwind.com/docs/react/sidebar
// - https://www.material-tailwind.com/docs/react/select

export default function FilterSideBar({ cantons, timeRanges, directions, vehicleTypes, onApplyFilterSettings }: Props) {

    function publishFilterSettings() {
        const settings: FilterSettings = {
            canton: selectedCanton,
            timeRange: selectedTimeRange,
            direction: selectedDirection,
            vehicleType: selectedVehicleType
        };
        onApplyFilterSettings(settings);
    }

    const [selectedCanton, setSelectedCanton] = useState<string | undefined>(cantons[0]);
    const [selectedTimeRange, setSelectedTimeRange] = useState<string | undefined>(timeRanges.length > 0 ? timeRanges[0].value : "No Time Range specified");
    const [selectedDirection, setSelectedDirection] = useState<string | undefined>(directions.length > 0 ? directions[0].value : "No Direction specified");
    const [selectedVehicleType, setSelectedVehicleType] = useState<string | undefined>(vehicleTypes.length > 0 ? vehicleTypes[0].value : "No Vehicle Type specified");

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
                            cantons.map((c, index) => (<Option value={c} key={index}>{c}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Time" value={selectedTimeRange} onChange={setSelectedTimeRange}>
                        {
                            timeRanges.map((t, index) => (<Option value={t.value} key={index}>{t.label}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Vehicle Type" value={selectedVehicleType} onChange={setSelectedVehicleType}>
                        {
                            vehicleTypes.map((v, index) => (<Option value={v.value} key={index}>{v.label}</Option>))
                        }
                    </Select>

                    <Select variant="outlined" label="Select Direction" value={selectedDirection} onChange={setSelectedDirection}>
                        {
                            directions.map((d, index) => (<Option value={d.value} key={index}>{d.label}</Option>))
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