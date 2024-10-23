
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
    manageUser()
  }
})     

onMounted( () => {
  getTrips()
  getUsers()
  setTimeout(() => manageUser(), 2000)
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

watch(state, () => {
  state.users.map(user => {
    const [localPart, domain] = user.email.split('@');
    user['masked_email'] = (localPart.length > 2 && domain != undefined)
      ? localPart.slice(0, 2) + '***'  + `@${domain}`
      : user.email;
  })
})

const manageUser = () => {
  if (user.value.email !== undefined ){

    console.log('patching user store...')
    userStore.$patch( {user: user} )

    const filteredUsers = state.users.filter((tmp) => tmp.email === user.value.email)
    console.log('filteredUsers', filteredUsers)
    if (filteredUsers.length === 0) {
      saveUser(user.value.email)
    }
  }
}

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
</script>

<template>
    <code class="my-5 text-xl inline-block" v-if="isAuthenticated">🥳 Welcome {{ user.given_name }}! | <button @click="doLogout" class="p-1 rounded-md text-white bg-red-400 inline-block text-sm">Logout</button></code>
    <h1 class="my-5 text-xl">🏕️ Create Trip</h1>
     <form @submit.prevent="save">
        <input type="text" placeholder="Trip Name" v-model="form.title" class="p-2 border border-slate-200 rounded-md w-full">
        <input type="text" placeholder="Description" v-model="form.text" class="p-2 border border-slate-200 rounded-md w-full">
        <h1 class="my-5">👥 Add Member:</h1>
        <div v-for="(user, index) in state.users" class="user-checkbox-div flex items-center mb-1">
          <input type="checkbox" v-model="form.users" :id="'user-'+index" :value="user" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded">
          <label :for="'user-'+index" class="ms-1 text-sm font-medium text-gray-900">{{ user.masked_email }}</label>
        </div>
        <button type="submit" class="p-2 rounded-md text-white bg-teal-500 w-full">Save</button>
    </form>
    <br>
    <h1 v-if="state.trips.length > 0" class="my-5 text-xl">List Trip</h1>
    <TripItem
        v-for="trip in state.trips"
        :key="trip.id"
        :trip="trip"
        @delete-trip="onDeleteTrip"
    ></TripItem>
</template>

<style>
/* .user-checkbox {
  display: inline;
}

.user-checkbox-div {
  text-align: left;
} */

a {
  cursor: pointer;
}
</style>