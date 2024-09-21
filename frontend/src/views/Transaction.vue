<script setup>
import { reactive, onMounted } from 'vue'

const form = reactive({
  user_email: '',
  title: '',
  cost: 0
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
  .then(data => console.log(data))
  .catch(error => console.error(error));
}

onMounted(async () => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => console.log(data))
    .catch(error => console.error(error));
})
</script>

<template>
  <form @submit.prevent="save">
    <input type="text" placeholder="user email" v-model="form.user_email">
    <input type="text" placeholder="title" v-model="form.title">
    <input type="number" min="0" placeholder='cost' v-model="form.cost">
    <button type="submit">Save</button>
  </form>
</template>

<style>
select,
input,
button {
  display: block;
  margin: 0.5em 0.5em;
  font-size: 15px;
}
</style>