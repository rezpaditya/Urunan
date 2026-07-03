
<script setup>
import { reactive, onMounted, watch } from 'vue'
import TripItem from '../components/TripItem.vue'
import { useAuth0 } from '@auth0/auth0-vue';
import { useUserStore } from '../stores/user'
import { Multiselect } from 'vue-multiselect'


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
    users: [],
    toggleAddTrip: false,
    currentUser: {},
})

const form = reactive({
  title: '',
  text: '',
  users: [],
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
    const loggedInUser = state.users.find((item) => item.email === user.value.email)
    if (loggedInUser === undefined) {
      // Save it if a new user
      saveUser(user.value.email)
    } else {
      state.currentUser = loggedInUser
			state.users = state.users.filter((item) => item.email != state.currentUser.email)
      // TODO: move this filter to BE
      const isUserIncluded = (users) => Boolean(users.find((user) => user.email === state.currentUser.email))
      state.trips = state.trips.filter((trip) => isUserIncluded(trip.users))
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
  // push the logged in user to the form
	form.users.push(state.currentUser)
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
    form.users = []
    state.toggleAddTrip = !state.toggleAddTrip
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

const optionUsers = ({email, id, masked_email}) => {
  return email
}

</script>

<template>
    <code class="my-5 text-xl inline-block" v-if="isAuthenticated">🏕️ Welcome, {{ user.given_name }}! | <button @click="doLogout" class="p-1 rounded-md text-white bg-red-400 inline-block text-sm">Logout</button></code>
    <hr>
    <h1 class="my-5 text-xl font-semibold">🧳 Your Trips</h1>
    <span @click="state.toggleAddTrip=!state.toggleAddTrip" class=" cursor-pointer block p-2 my-2 w-full rounded-md border border-dashed border-slate-200 bg-slate-50">+ Create New Trip</span>
    <div v-if="state.toggleAddTrip">
      <form @submit.prevent="save">
          <input type="text" required placeholder="Trip Name" v-model="form.title" class="p-2 border border-slate-200 rounded-md w-full">
          <input type="text" placeholder="Description (optional)" v-model="form.text" class="p-2 border border-slate-200 rounded-md w-full">
          <Multiselect v-model="form.users" 
            :options="state.users" 
            :custom-label="optionUsers" optionLabel="name" placeholder="-- Invite Users --"
            :multiple="true" :close-on-select="false" :clear-on-select="false"
            track-by="id">
            <template #selection="{ values, search, isOpen }">
              <span class="multiselect__single"
                    v-if="values.length"
                    v-show="!isOpen">{{ values.length }} options selected</span>
            </template>
          </Multiselect>
          <button type="submit" class="p-2 mb-16 rounded-md text-white bg-teal-500 w-full">Save</button>
      </form>
    </div>
    <template v-if="Object.keys(state.currentUser).length > 0">
      <TripItem
          v-for="trip in state.trips"
          :key="trip.id"
          :trip="trip"
          @delete-trip="onDeleteTrip"
      ></TripItem>
    </template>
</template>

<style>
a {
  cursor: pointer;
}
</style>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>