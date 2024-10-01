
<script setup>
import { reactive, onMounted } from 'vue'
import TripItem from '../components/TripItem.vue'

const state = reactive({
    trips: [],
    users: []
})

const form = reactive({
  title: '',
  text: '',
  users: []
})

const getTrips = async () => {
  // TODO: refactor the try-catch for other http requests
  try {
    fetch(`${import.meta.env.VITE_API_URL}/trips`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(response => response.json())
      .then(data => state.trips = data)
      .catch(error => console.error(error));
  } catch(e) {
    console.error(e)
  }
}

const getUsers = async () => {
  // TODO: move https request to some kind of service module
  try {
    fetch(`${import.meta.env.VITE_API_URL}/users`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(response => response.json())
      .then(data => state.users = data)
      .catch(error => console.error(error));
  } catch(e) {
    console.error(e)
  }
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
    users: form.users
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
  getUsers()
})
</script>

<template>
     <form @submit.prevent="save">
        <input type="text" placeholder="trip name" v-model="form.title">
        <input type="text" placeholder="description" v-model="form.text">
        <div v-for="(user, index) in state.users" class="user-checkbox-div">
          <label :for="'user-'+index">
            <input type="checkbox" v-model="form.users" :id="'user-'+index" :value="user" class="user-checkbox">
            <span>{{ user.email }}</span>
          </label>
        </div>
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
.user-checkbox {
  display: inline;
}

.user-checkbox-div {
  text-align: left;
}
</style>