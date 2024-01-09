const TIME_RANGES = [
    {
        label: "Last 10 Minutes",
        value: "-10m",
        binSize: "1m"
    },
    {
        label: "Last Hour",
        value: "-1h",
        binSize: "10m"
    },
    {
        label: "Last 4 Hours",
        value: "-4h",
        binSize: "30m"
    },
    {
        label: "Last Day",
        value: "-24h",
        binSize: "1h"
    },
    {
        label: "Last Week",
        value: "-7d",
        binSize: "1d"
    }
];

const DEFAULT_BIN_SIZE = "1m";

const DIRECTIONS = [
    {
        label: "Positive",
        value: "positive"
    },
    {
        label: "Negative",
        value: "negative"
    },
];

const VEHICLE_TYPES = [
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


export const FILTER_VALUE_MAP = {
    "cantons": {
        "values": [],
        "default": "all"
    },
    "timeRanges": {
        "values": TIME_RANGES,
        "default": TIME_RANGES[0].value
    },
    "directions": {
        "values": DIRECTIONS,
        "default": DIRECTIONS[0].value
    },
    "vehicleTypes": {
        "values": VEHICLE_TYPES,
        "default": VEHICLE_TYPES[0].value
    }
}

export function getBinSizeForTimeRangeValue(timeRangeValue) {
    const index = TIME_RANGES.findIndex(t => t.value === timeRangeValue);
    if (index < 0) {
        console.warn(`Did not find corresponding Time Range for value ${timeRangeValue}, default bin size will be returned`);
        return DEFAULT_BIN_SIZE;
    }
    return TIME_RANGES[index].binSize;
}

export const DEFAULT_FILTER_SETTINGS = {
    canton: "all",
    timeRange: FILTER_VALUE_MAP.timeRanges.default,
    direction: FILTER_VALUE_MAP.directions.default,
    vehicleType: FILTER_VALUE_MAP.vehicleTypes.default,
}