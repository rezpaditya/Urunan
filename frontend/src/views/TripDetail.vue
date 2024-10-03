
<script setup>
import { reactive, onMounted, computed, watch } from 'vue'
import TransactionItem from '../components/TransactionItem.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const tripId = route.params.id;

const state = reactive({
    trip: {},
    transactions: [],
})

const form = reactive({
  email: '',
  title: '',
  cost: 0,
  details: []
})

watch(form, (newValue) => {
  state.trip.users.map(user => {
    user['cost'] = Math.round(form.cost / state.trip.users.length)
  })
})

onMounted(() => {
  getTransaction()
})

const getTransaction = async () => {
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
        // DEBUG
        console.log(state.trip.transactions)
    })
    .catch(error => console.error(error));
}

const save = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: form.email,
      title: form.title,
      cost: form.cost,
      trip_id: tripId,
      details: state.trip.users
    })
  })
  .then(response => response.json())
  .then(data => {
    state.transactions.push(data)
    form.email = ''
    form.title = ''
    form.cost = 0
  })
  .catch(error => console.error(error));
}

const onDeleteTransaction = async (transactionId) => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/${transactionId}`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data === true) {
        // TODO: only update the fe state instead of pulling from be
        getTransaction() 
      }
    })
    .catch(error => console.error(error));
}
</script>

<template>
    <form @submit.prevent="save">
       <select v-model="form.email">
        <option v-for="user in state.trip.users" :value="user.email">{{ user.email }}</option>
       </select>
      <input type="text" placeholder="transaction name" v-model="form.title">
      <input type="number" min="0" placeholder='cost' v-model="form.cost">
      <div v-for="(user, index) in state.trip.users">
        <label :for="'user-'+index">
          <span>{{ user.email }}</span>
          <input type="hidden" v-model="user.id">
          <input type="number" min="0" placeholder='cost' class="user-portion" v-model="user.cost">
        </label>
      </div>
      <button type="submit">Save</button>
    </form>
    <TransactionItem
        v-for="transactions in state.transactions"
        :key="transactions.id"
        :transaction="transactions"
        @delete-transaction="onDeleteTransaction"
    ></TransactionItem>
</template>

<style>
.user-portion {
  display: inline-block;
}
</style>