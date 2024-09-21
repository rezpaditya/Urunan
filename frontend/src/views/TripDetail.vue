
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

const form = reactive({
  user_email: '',
  title: '',
  cost: 0
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

const save = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    user_email: form.user_email,
    title: form.title,
    cost: form.cost,
    trip_id: 1
  })
})
  .then(response => response.json())
  .then(data => {
    state.transactions.push(data)
    form.user_email = ''
    form.title = ''
    form.cost = 0
  })
  .catch(error => console.error(error));
}
</script>

<template>
    <form @submit.prevent="save">
      <input type="text" placeholder="example@email.com" v-model="form.user_email">
      <input type="text" placeholder="Bayar makan siang" v-model="form.title">
      <input type="number" min="0" placeholder='50' v-model="form.cost">
      <button type="submit">Save</button>
    </form>
    <TransactionItem
        v-for="transactions in state.transactions"
        :key="transactions.id"
        :transaction="transactions"
    ></TransactionItem>
</template>

<style>
</style>