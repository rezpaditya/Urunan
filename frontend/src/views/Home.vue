<script setup>
import { onMounted } from 'vue'
import { useAuth0 } from '@auth0/auth0-vue';
import { useRouter } from 'vue-router'


const router = useRouter()
const { loginWithRedirect, isAuthenticated, user } = useAuth0();
const login = () => {
        loginWithRedirect();
    }

onMounted(() => {
    setTimeout(() => checkUser(), 2000)
})

const checkUser = () => {
    if (user.value) {
        console.log('authenticated...', user)
        router.push({ name: 'trip' })
    }
}
</script>

<template>
    <div>
        <h3>Click the button below to continue.</h3>
        <button @click="login" class="p-2 rounded-md text-white bg-teal-500">Log in</button>
    </div>
</template>

<style scoped>
</style>