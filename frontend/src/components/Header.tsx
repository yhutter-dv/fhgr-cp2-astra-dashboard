import { ChartBarIcon } from "@heroicons/react/20/solid";
import {
    Navbar, Switch,
} from "@material-tailwind/react";
import { useState } from "react";

type Props = {
    onLiveModeChanged: (liveModeEnabled: boolean) => void;
}


// Implemented with reference to: https://www.material-tailwind.com/docs/react/navbar
export default function Header({ onLiveModeChanged }: Props) {


    function publishOnLiveModeChanged(liveModeEnabled: boolean) {
        setLiveModeEnabled(liveModeEnabled);
        onLiveModeChanged(liveModeEnabled);
    }

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
                <Switch checked={liveModeEnabled} onChange={e => publishOnLiveModeChanged(e.target.checked)} label="Automatic Update" crossOrigin={undefined} />
            </div>
        </Navbar>
    );
}