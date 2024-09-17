<script setup>
import { ref } from 'vue'

const email = ref('')
const description = ref('')
const cost = ref(0)

function save() {
  alert('submit form...')
}
</script>

<template>
  <input type="text" placeholder="author email" v-model="email">
  <input type="text" placeholder="description" v-model="description">
  <input type="number" min="0" placeholder='cost' v-model="cost">
  <button @click="save">Save</button>
</template>

<style>
select,
input,
button {
  display: block;
  margin: 0.5em 0;
  font-size: 15px;
}
</style>