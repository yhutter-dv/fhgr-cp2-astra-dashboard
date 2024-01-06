<script>
    import { createEventDispatcher } from "svelte";

    export let elements = [];

    const dispatch = createEventDispatcher();

    function onSelectionChanged(e) {
        dispatch("selectionChanged", {
            selected: e.target.value,
        });
    }
</script>

<select
    class="w-full rounded-md shadow-sm border border-slate-500"
    on:change={onSelectionChanged}
>
    {#each elements as element}
        <option class="py-2" value={element.value}>{element.label}</option>
    {/each}
</select>
