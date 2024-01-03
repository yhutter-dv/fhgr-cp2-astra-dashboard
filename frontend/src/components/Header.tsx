import { ChartBarIcon } from '@heroicons/react/24/solid'


export default function Header() {
    return (
        <div className="fixed z-50 bg-white w-full py-6 px-8 flex flex-col sm:flex-row items-center gap-4 shadow-sm">
            <div className="flex items-center flex-1">
                <ChartBarIcon className="h-8 w-8 text-blue-500" />
                {/* <IconBallTennis aria-hidden="true" /> */}
                <div className="text-2xl ml-1 font-bold">
                    Astra Dashboard
                </div>
            </div>
        </div>
    );
}