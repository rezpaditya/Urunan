<script setup>
defineProps({trip: Object})
</script>

<template>
  <div class="block p-2 my-2 w-full rounded-md border border-slate-200">
   <RouterLink
      :to="{ name: 'trip-detail', params: {id: trip.id} }"
      >{{ trip.title }} - {{ trip.text }}
    </RouterLink>
    <span @click="$emit('deleteTrip', trip.id)" class="font-extrabold"> ❌</span>
  </div>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>