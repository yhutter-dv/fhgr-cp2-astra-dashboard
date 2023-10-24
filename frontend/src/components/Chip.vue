<script setup lang="ts">

defineProps<{ text: string }>()

</script>

<template>
    <span
        class="inline-flex items-center rounded-md bg-sky-50 px-2 py-1 text-xs font-medium text-sky-700 ring-1 ring-inset ring-sky-700/10">{{ text }}</span>
</template>

<style scoped></style>
