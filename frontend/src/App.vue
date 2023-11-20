<script setup lang="ts">
import { ref } from "vue"
import Header from './components/Header.vue'
import Map from './components/Map.vue'
import Sidebar from './components/Sidebar.vue'

const sidebarVisible = ref(true)
const sidebar = ref<InstanceType<typeof Sidebar> | null>(null)

const vehicleTypes = [
    "Truck",
    "Car"
]

const toggleSidebarVisibility = (visibility: boolean) => {
    sidebarVisible.value = visibility
    sidebar.value?.setVisibility(visibility)
}

</script>

<template>
    <div class="w-full">
        <Header @filter-clicked="toggleSidebarVisibility"></Header>
        <Sidebar ref="sidebar" :vehicle-types="vehicleTypes"></Sidebar>
        <div :class="{ 'ml-0': !sidebarVisible, 'ml-[20rem]': sidebarVisible }" class="p-4">
            <div class="grid grid-cols-3 gap-4">
                <div class="p-4 shadow rounded bg-white col-span-2 h-half">
                    <h3 class="font-semibold text-medium mb-2">Map</h3>
                    <Map></Map>
                </div>

                <div class="p-4 shadow rounded bg-white">
                    <h3 class="font-medium text-md mb-2">Chart 1</h3>
                    <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nemo incidunt voluptas
                        repellendus libero
                        blanditiis ipsa quam asperiores doloremque quas sunt, reiciendis ipsum veritatis tempora, alias
                        temporibus aut dicta, neque sed.</p>
                </div>

                <div class="p-4 shadow rounded bg-white col-span-3 h-48">
                    <h3 class="font-medium text-md mb-2">Scarf Plot</h3>
                    <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nemo incidunt voluptas
                        repellendus libero
                        blanditiis ipsa quam asperiores doloremque quas sunt, reiciendis ipsum veritatis tempora, alias
                        temporibus aut dicta, neque sed.</p>
                </div>
                <div class="p-4 shadow rounded bg-white col-span-3 h-48">
                    <h3 class="font-medium text-md mb-2">Scarf Plot</h3>
                    <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nemo incidunt voluptas
                        repellendus libero
                        blanditiis ipsa quam asperiores doloremque quas sunt, reiciendis ipsum veritatis tempora, alias
                        temporibus aut dicta, neque sed.</p>
                </div>
                <div class="p-4 shadow rounded bg-white col-span-3 h-48">
                    <h3 class="font-medium text-md mb-2">Scarf Plot</h3>
                    <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nemo incidunt voluptas
                        repellendus libero
                        blanditiis ipsa quam asperiores doloremque quas sunt, reiciendis ipsum veritatis tempora, alias
                        temporibus aut dicta, neque sed.</p>
                </div>
                <div class="p-4 shadow rounded bg-white col-span-3 h-48">
                    <h3 class="font-medium text-md mb-2">Scarf Plot</h3>
                    <p class="text-sm">Lorem ipsum dolor sit amet, consectetur adipisicing elit. Nemo incidunt voluptas
                        repellendus libero
                        blanditiis ipsa quam asperiores doloremque quas sunt, reiciendis ipsum veritatis tempora, alias
                        temporibus aut dicta, neque sed.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped></style>
