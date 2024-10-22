<script setup>
defineProps({trip: Object})
</script>

<template>
   <RouterLink
        :to="{ name: 'trip-detail', params: {id: trip.id} }"
        class="block p-2 my-2 w-full rounded-md border border-slate-200"
        >{{ trip.title }} - {{ trip.text }}
        <span @click="$emit('deleteTrip', trip.id)" class="font-extrabold"> ❌</span>
      </RouterLink>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>