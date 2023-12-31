import { writable } from 'svelte/store';

// See: https://svelte.dev/docs/svelte-store
export const trafficFlowMeasurements = writable([]);
export const trafficSpeedMeasurements = writable([]);
export const numberOfErrorsPerCantonMeasurements = writable([]);
export const cantons = writable([]);
export const selectedStation = writable(null);
export const stationsWithTotalNumberOfErrorsPerCanton = writable({
    "stations": [],
    "totalNumberOfErrorsPerCanton": []
});