const TIME_RANGES = [
    {
        label: "Last 4 hours",
        value: "-4h"
    },
    {
        label: "Last 8 hours",
        value: "-8h"
    },
    {
        label: "Last Day",
        value: "-1d"
    },
    {
        label: "Last Week",
        value: "-7d"
    },
    {
        label: "Last Month",
        value: "-30d"
    }
];

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

export const DEFAULT_FILTER_SETTINGS = {
    canton: "all",
    timeRange: FILTER_VALUE_MAP.timeRanges.default,
    direction: FILTER_VALUE_MAP.directions.default,
    vehicleType: FILTER_VALUE_MAP.vehicleTypes.default,
}