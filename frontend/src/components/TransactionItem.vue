<script setup>
defineProps({transaction: Object, isTripSettled: Boolean})
</script>

<template>
  <RouterLink 
    :to="{ name: 'transaction-detail', params: {id: transaction.id} }"
    class="block p-2 my-2 w-full rounded-md border border-slate-200">{{ transaction.title }} €{{ transaction.cost }} - paid by {{ transaction.email }}
    <span v-if="!isTripSettled" @click="$emit('deleteTransaction', transaction.id)"> ❌</span>
  </RouterLink>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>