
<script setup>
import { reactive, onMounted } from 'vue'
import TripItem from '../components/TripItem.vue'

const state = reactive({
    trips: []
})

const form = reactive({
  title: '',
  text: ''
})

const getTrips = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => state.trips = data)
    .catch(error => console.error(error));
}

const save = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    title: form.title,
    text: form.text,
    users: {
        email: 'dummy@email.com'
    }
  })
})
  .then(response => response.json())
  .then(data => {
    state.trips.push(data)
    form.title = ''
    form.text = ''
  })
  .catch(error => console.error(error));
}

const onDeleteTrip = async (tripId) => {
  fetch(`${import.meta.env.VITE_API_URL}/trips/${tripId}`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data === true) {
        // TODO: only update the fe state instead of pulling from be
        getTrips() 
      }
    })
    .catch(error => console.error(error));
}

onMounted( () => {
  getTrips()
})
</script>

<template>
     <form @submit.prevent="save">
        <input type="text" placeholder="trip name" v-model="form.title">
        <input type="text" placeholder="description" v-model="form.text">
        <button type="submit">Save</button>
    </form>
    <TripItem
        v-for="trip in state.trips"
        :key="trip.id"
        :trip="trip"
        @delete-trip="onDeleteTrip"
    ></TripItem>
</template>

<style>
</style>