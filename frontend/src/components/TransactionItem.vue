<script setup>
defineProps({transaction: Object, isTripSettled: Boolean})
</script>

<template>
  <p>{{ transaction.title }} €{{ transaction.cost }} - paid by {{ transaction.email }}
    <span v-if="!isTripSettled" @click="$emit('deleteTransaction', transaction.id)"> X</span>
  </p>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>