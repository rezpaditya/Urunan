<script setup>
defineProps({transaction: Object, isTripSettled: Boolean})
</script>

<template>
  <div class="block p-2 my-2 w-full rounded-md border border-slate-200">
    <RouterLink 
      :to="{ name: 'transaction-detail', params: {id: transaction.id} }"
      >{{ transaction.title }} €{{ transaction.cost }} - paid by {{ transaction.email }}
    </RouterLink>
    <span v-if="!isTripSettled" @click="$emit('deleteTransaction', transaction.id)"> ❌</span>
  </div>
</template>

<style scoped>
  span {
    color: red;
    cursor: pointer;
  }
</style>