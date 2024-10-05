<script setup>
defineProps({transaction: Object})
</script>

<template>
  <p>{{ transaction.title }} €{{ transaction.cost }} - paid by {{ transaction.email }}
    <span @click="$emit('deleteTransaction', transaction.id)"> X</span>
  </p>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>