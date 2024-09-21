
<script setup>
import { reactive, onMounted } from 'vue'
import TripItem from '../components/TripItem.vue'

const state = reactive({
    trips: []
})

onMounted(async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => state.trips = data)
    .catch(error => console.error(error));
})
</script>

<template>
    <TripItem
        v-for="trip in state.trips"
        :key="trip.id"
        :title="trip.title"
        :text="trip.text"
    ></TripItem>
</template>

<style>
</style>