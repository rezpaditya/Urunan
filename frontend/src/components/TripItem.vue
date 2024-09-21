<script setup>
defineProps({trip: Object})
</script>

<template>
  <h4>{{ trip.title }} - {{ trip.text }}</h4>
  <RouterLink
    :to="`/${trip.id}`"
    >Detail
  </RouterLink>
</template>