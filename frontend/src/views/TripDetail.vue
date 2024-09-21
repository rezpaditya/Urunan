
<script setup>
import { reactive, onMounted } from 'vue'
import TransactionItem from '../components/TransactionItem.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const tripId = route.params.id;

const state = reactive({
    trip: null,
    transactions: []
})

onMounted(async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips/${tripId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => {
        state.trip = data
        state.transactions = data.transactions
    })
    .catch(error => console.error(error));
})
</script>

<template>
    <TransactionItem
        v-for="transactions in state.transactions"
        :key="transactions.id"
        :transaction="transactions"
    ></TransactionItem>
</template>

<style>
</style>