
<script setup lang="ts">
import { ref } from "vue"
import SelectableChip from "./SelectableChip.vue"
import PrimaryButton from "./PrimaryButton.vue"


const props = defineProps<{ vehicleTypes: string[] }>()
const isVisible = ref(true)

const onVehicleTypeClicked = (vehicleType: string, active: boolean) => {
    console.log(`Clicked ${vehicleType}, active: ${active}`)
}
const setVisibility = (visible: boolean) => {
    isVisible.value = visible
}

defineExpose({
    setVisibility
})
</script>

<template>
    <div :class="{ 'hidden': !isVisible }"
        class="transition ease-in-out duration-150 fixed top-16 p-4 border-r h-full overflow-y-auto max-w-xs shadow">
        <h2 class="mb-2 text-sm leading-6 font-semibold text-sky-500">Vehicle Type
        </h2>
        <p class="text-sm text-slate-500 mb-4">Here you can choose which vehicle types you are interested in</p>

        <div class="flex items-center space-x-4">
            <SelectableChip v-for="vehicleType in props.vehicleTypes" :text="vehicleType" @clicked="onVehicleTypeClicked">
            </SelectableChip>
        </div>

        <h2 class="mt-4 mb-2 text-sm leading-6 font-semibold text-sky-500">
            Measurement
            Station
        </h2>
        <p class="text-sm text-slate-500 mb-4">Choose the Measurement Station you are interested in. We also have
            autocomplete so type away.</p>
        <PrimaryButton text="Apply Filter"></PrimaryButton>
    </div>
</template>

<style scoped></style>
