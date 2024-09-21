import { createRouter, createWebHistory } from 'vue-router';
import TripView from '../views/Trip.vue';
import TripDetailView from '../views/TripDetail.vue';
import TransactionView from '../views/Transaction.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'trip',
      component: TripView,
    },
    {
      path: '/:id',
      name: 'trip-detail',
      component: TripDetailView,
    },
    {
      path: '/transaction',
      name: 'transaction',
      component: TransactionView,
    },
  ],
});

export default router;