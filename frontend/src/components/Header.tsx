import { ChartBarIcon } from "@heroicons/react/20/solid";
import {
    Navbar, Switch,
} from "@material-tailwind/react";
import { useState } from "react";

// Implemented with reference to: https://www.material-tailwind.com/docs/react/navbar
export default function Header() {
    const [liveModeEnabled, setLiveModeEnabled] = useState<boolean>(true);

    return (
        <Navbar className="sticky top-0 z-50 h-max max-w-full  py-6 px-8 rounded-none">
            <div className="flex items-center justify-between flex-row text-blue-gray-900">
                <div className="flex">
                    <ChartBarIcon className="h-8 w-8 text-black" />
                    <p className="text-2xl ml-1 font-bold">
                        Astra Dashboard
                    </p>
                </div>
                <Switch checked={liveModeEnabled} onChange={e => setLiveModeEnabled(e.target.checked)} label="Automatic Update" crossOrigin={undefined} />
            </div>
        </Navbar>
    );
}