<script setup>
defineProps({transaction: Object})
</script>

<template>
  <h4>{{ transaction.title }} - {{ transaction.cost }}</h4>
</template>