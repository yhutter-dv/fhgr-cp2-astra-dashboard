<script setup lang="ts">
import { ref } from 'vue'


const props = defineProps<{ text: string}>()
const emit = defineEmits(['clicked'])
const active = ref(false)

const toggleActive = () => {
    active.value = !active.value
    emit("clicked", props.text, active.value)
}

</script>

<template>
    <span
        @click="toggleActive"
        :class="{ 'bg-sky-700 text-white' : active}"
        class="transition-colors inline-flex hover:cursor-pointer items-center rounded-md bg-sky-50 px-2 py-1 text-xs font-medium text-sky-700 ring-1 ring-inset ring-sky-700/10">{{
            text }}</span>
</template>

<style scoped></style>
