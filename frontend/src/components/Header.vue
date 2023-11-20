<script setup lang="ts">
import { ref } from "vue"
import Chip from './Chip.vue'

const emit = defineEmits(['filter-clicked'])
const filterActive = ref(true)

const toggleFilter = () => {
    filterActive.value = !filterActive.value
    emit("filter-clicked", filterActive.value)
}

</script>

<template>
    <div class="h-16 flex items-center space-x-4 sticky top-0 p-4 border-b bg-transparent z-40 backdrop-blur">
        <svg @click="toggleFilter" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" :class="{ 'fill-sky-400': filterActive }"
            class="w-6 h-6 hover:cursor-pointer stroke-sky-400">
            <path stroke-linecap="round" stroke-linejoin="round"
                d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z" />
        </svg>

        <h1 class="text-xl font-medium">Astra Dashboard</h1>
        <Chip text="Made with Tailwind"></Chip>
        <div class="grow flex items-center justify-end">
            <a class="hover:text-sky-500 font-normal" href="#">Feedback</a>
        </div>
    </div>
</template>

<style scoped></style>

