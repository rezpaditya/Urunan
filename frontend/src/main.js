import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { createAuth0 } from '@auth0/auth0-vue'

const app = createApp(App)

app.use(router);
app.use(
    createAuth0({
        domain: "dev-tnt2lmw4xher1ebe.us.auth0.com",
        clientId: "eeZdeGPs3AsclvulqdGhvzSO82yRkvGF",
        authorizationParams: {
            redirect_uri: window.location.origin
        }
        })
  );

app.mount('#app')
