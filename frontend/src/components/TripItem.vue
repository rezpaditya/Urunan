<script setup>
defineProps({trip: Object})
</script>

<template>
  <p>
    <RouterLink
        :to="{ name: 'trip-detail', params: {id: trip.id} }"
        >{{ trip.title }} - {{ trip.text }}
      </RouterLink>
      <span @click="$emit('deleteTrip', trip.id)"> X</span>
  </p>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>