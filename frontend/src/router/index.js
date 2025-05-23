import { createRouter, createWebHashHistory } from 'vue-router';
import TripView from '../views/Trip.vue';
import TripDetailView from '../views/TripDetail.vue';
import TransactionView from '../views/Transaction.vue';
import TransactionDetailView from '../views/TransactionDetail.vue';
import HomeView from '../views/Home.vue';
import { authGuard } from '@auth0/auth0-vue';


const router = createRouter({
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/trip',
      name: 'trip',
      component: TripView,
      beforeEnter: authGuard,
    },
    {
      path: '/trip/:id',
      name: 'trip-detail',
      component: TripDetailView,
      beforeEnter: authGuard,
    },
    {
      path: '/transaction',
      name: 'transaction',
      component: TransactionView,
      beforeEnter: authGuard,
    },
    {
      path: '/transaction/:id',
      name: 'transaction-detail',
      component: TransactionDetailView,
      beforeEnter: authGuard,
    },
  ],
});

export default router;