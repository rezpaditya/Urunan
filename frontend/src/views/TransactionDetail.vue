<script setup>
import { reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'


const route = useRoute()
const router = useRouter()
const transactionId = route.params.id;

const state = reactive({
  transaction: {}
})
const form = reactive({
  user_email: '',
  title: '',
  cost: 0,
  file: null
})

const setFile = ($event) => {
  if ($event.target && $event.target.files) {
      form.file = $event.target.files[0];
      console.log(form.file)
  }
}

const update = async () => {
  const params = new URLSearchParams({
    'id': transactionId,
    'title': state.transaction.title,
    'transaction_date': state.transaction.transaction_date
  });

  const formData = new FormData();
  formData.append('file', form.file);

  fetch(`${import.meta.env.VITE_API_URL}/transactions/?${params}`, {
    method: 'PATCH',
    headers: {
      'accept': 'application/json',
    },
    body: formData
  })
  .then(response => {
    (response.ok) ? router.go(-1) : alert('Oops! Something when wrong!')
  })
  .catch(error => console.error(error));
}

onMounted(async () => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/${transactionId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => {
      state.transaction = data
      state.transaction.transaction_date = state.transaction.transaction_date.split('T')[0]
    })
    .catch(error => console.error(error));
})
</script>

<template>
  <h1 class="my-5 text-xl">Payer: {{ state.transaction.email }}</h1>
  <h1 class="my-5 text-xl">Cost: €{{ state.transaction.cost }}</h1>
  <form @submit.prevent="update">
    <label class="text-xs">Transation Title</label>
    <input v-model="state.transaction.title" type="text" placeholder="Transaction title" class="p-2 block w-full border border-slate-200 rounded-md">
    <label class="text-xs">Transation Date</label>
    <input v-model="state.transaction.transaction_date" type="date" placeholder="Transaction date" class="p-2 block w-full border border-slate-200 rounded-md">
    
    <br>
    <a v-if="state.transaction.receipt" href="#">Download Receipt</a>
    <input type="file" @change="setFile($event)" placeholder="Receipt" class="p-2 block w-full border border-slate-200 rounded-md">
    <button type="submit" class="p-2 rounded-md text-white bg-teal-500 w-full">Update</button>
  </form>
</template>

<style>
select,
input,
button {
  display: block;
  margin: 0.5em 0em;
  font-size: 15px;
}
</style>