<script setup lang="ts">
defineProps<{ text: string }>()
</script>

<template>
    <button class="p-2 hover:bg-slate-700 bg-slate-900 rounded text-white text-sm font-medium shadow">{{ text }}</button>
</template>

<style scoped></style>
