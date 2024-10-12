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
    checkUser()
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
        <h3>Click the Login Button to continue.</h3>
        <button @click="login">Log in</button>
    </div>
</template>

<style scoped>
button {
    background-color: rgb(81, 138, 138);
}
</style>