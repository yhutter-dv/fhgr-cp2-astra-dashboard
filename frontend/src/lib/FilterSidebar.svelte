<script>
    import { FILTER_VALUE_MAP } from "../utils/filterValues";
    import SelectBox from "./SelectBox.svelte";
    import { createEventDispatcher } from "svelte";

    export let cantons = [];

    const timeRanges = FILTER_VALUE_MAP.timeRanges.values;
    const directions = FILTER_VALUE_MAP.directions.values;
    const vehicleTypes = FILTER_VALUE_MAP.vehicleTypes.values;

    const dispatch = createEventDispatcher();

    let selectedCanton = null;
    let selectedTimeRange = FILTER_VALUE_MAP.timeRanges.default;
    let selectedDirection = FILTER_VALUE_MAP.directions.default;
    let selectedVehicleType = FILTER_VALUE_MAP.vehicleTypes.default;

    function selectedCantonChanged(canton) {
        selectedCanton = canton;
    }

    function selectedTimeRangeChanged(timeRange) {
        selectedTimeRange = timeRange;
    }

    function selectedDirectionChanged(direction) {
        selectedDirection = direction;
    }

    function selectedVehicleTypeChanged(vehicleType) {
        selectedVehicleType = vehicleType;
    }

    function onApplyFilter() {
        const filterSettings = {
            canton: selectedCanton || FILTER_VALUE_MAP.cantons.default,
            timeRange: selectedTimeRange,
            direction: selectedDirection,
            vehicleType: selectedVehicleType,
        };

        dispatch("applyFilter", {
            settings: filterSettings,
        });
    }
</script>

<div
    class="fixed top-0 left-0 z-40 w-64 pt-32 px-4 h-screen bg-white border border-r-1"
>
    <div class="flex flex-col gap-y-6">
        <p class="text-lg font-bold">Filter Settings</p>

        <div>
            <p class="font-medium text-lg mb-4">Canton</p>
            <SelectBox
                elements={cantons}
                on:selectionChanged={(e) =>
                    selectedCantonChanged(e.detail.selected)}
            />
        </div>

        <div>
            <p class="font-medium text-lg mb-4">Time Range</p>
            <SelectBox
                elements={timeRanges}
                on:selectionChanged={(e) =>
                    selectedTimeRangeChanged(e.detail.selected)}
            />
        </div>

        <div>
            <p class="font-medium text-lg mb-4">Direction</p>
            <SelectBox
                elements={directions}
                on:selectionChanged={(e) =>
                    selectedDirectionChanged(e.detail.selected)}
            />
        </div>

        <div>
            <p class="font-medium text-lg mb-4">Vehicle Types</p>
            <SelectBox
                elements={vehicleTypes}
                on:selectionChanged={(e) =>
                    selectedVehicleTypeChanged(e.detail.selected)}
            />
        </div>

        <div class="mt-4">
            <button
                class="w-full bg-blue-500 p-2 rounded shadow-md text-white font-bold"
                on:click={onApplyFilter}>Apply Filter</button
            >
        </div>
    </div>
</div>
