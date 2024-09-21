<script setup>
defineProps({trip: Object})
</script>

<template>
  <h4>
    <RouterLink
      :to="`/${trip.id}`"
      >{{ trip.title }} - {{ trip.text }}
    </RouterLink>
  </h4>
</template>