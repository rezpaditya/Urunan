
<script setup>
import { reactive, onMounted, watch } from 'vue'
import TripItem from '../components/TripItem.vue'
import { useAuth0 } from '@auth0/auth0-vue';
import { useUserStore } from '../stores/user'


const userStore = useUserStore()
const { logout, user, isAuthenticated } = useAuth0();
const doLogout = () => {
                      logout({ logoutParams: { returnTo: window.location.origin } });
                    }


watch(user, () => {
  if(isAuthenticated && user.value){
    if (user.value.email !== undefined ){

      console.log('patching user store...')
      userStore.$patch( {user: user} )

      const filteredUsers = state.users.filter((tmp) => tmp.email === user.value.email)
      if (filteredUsers.length === 0) {
        saveUser(user.value.email)
      }
    }
  }
})       

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

const saveUser = async (email) => {
  fetch(`${import.meta.env.VITE_API_URL}/users/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: email
    })
})
  .then(response => response.json())
  .then(data => {
    state.users.push(data)
  })
  .catch(error => console.error(error));
}

onMounted( () => {
  getTrips()
  getUsers()
  console.log('patching user store...')
  userStore.$patch( {user: user} )
})
</script>

<template>
    <pre v-if="isAuthenticated">
      <code>Welcome {{ user.given_name }} | <a @click="doLogout">Logout</a></code>
    </pre>

    <h3>Create Trip</h3>
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

a {
  cursor: pointer;
}
</style>