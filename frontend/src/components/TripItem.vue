<script setup>
defineProps({trip: Object})
</script>

<template>
   <RouterLink
        :to="{ name: 'trip-detail', params: {id: trip.id} }"
        class="block shadow-md p-4 w-full rounded-md"
        >{{ trip.title }} - {{ trip.text }}
        <span @click="$emit('deleteTrip', trip.id)" class="font-extrabold"> X</span>
      </RouterLink>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>