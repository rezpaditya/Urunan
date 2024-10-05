
<script setup>
import { reactive, onMounted, computed, watch } from 'vue'
import TransactionItem from '../components/TransactionItem.vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const tripId = route.params.id;

const state = reactive({
    trip: {},
    transactions: [],
    users: [],
    currentUser: 'user1',
})

const form = reactive({
  email: '',
  title: '',
  cost: 0,
  details: []
})

watch(form, () => {
  state.trip.users.map(user => {
    user['cost'] = Math.round(form.cost / state.trip.users.length)
  })
})

onMounted(() => {
  getTransaction()
})

const userPaid = computed(() => {
  const userPaid = transaction => transaction.email === state.currentUser ? transaction.cost : 0;
  return state.transactions.reduce((total, transaction) => total + userPaid(transaction), 0);
})

const mappedDebt = computed(() => {
  const userExpenses = {};
  state.users.forEach(user => {
      userExpenses[user.email] = 0; 
  });
  state.transactions.forEach(transaction => {
      transaction.details.forEach(portion => {
          userExpenses[portion.email] += portion.cost;
      });
  });
  
  const userDebt = {};
  state.users.forEach(user => {
      const userPaid = transaction => transaction.email === user.email ? transaction.cost : 0;
      const totalPaidByUser = state.transactions.reduce((total, transaction) => total + userPaid(transaction), 0);
      const totalUserExpense = userExpenses[user.email];
      userDebt[user.email] = totalPaidByUser - totalUserExpense;
  });

  const mappedDebt = [];
  state.users.forEach(borrower => {
      state.users.forEach(lender => {
          if (borrower !== lender) {
              const amountOwed = Math.min(userDebt[borrower.email], -userDebt[lender.email]);
              if (amountOwed > 0) {
                  mappedDebt.push({
                      from: borrower.email,
                      to: lender.email,
                      amount: amountOwed
                  });
                  userDebt[borrower] -= amountOwed;
                  userDebt[lender] += amountOwed;
              }
          }
      });
  });
  return mappedDebt
})

const getTransaction = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips/${tripId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  })
    .then(response => response.json())
    .then(data => {
        state.trip = data
        state.transactions = data.transactions
        state.users = data.users
    })
    .catch(error => console.error(error));
}

const save = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/transactions/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      email: form.email,
      title: form.title,
      cost: form.cost,
      trip_id: tripId,
      details: state.trip.users
    })
  })
  .then(response => response.json())
  .then(data => {
    state.transactions.push(data)
    form.email = ''
    form.title = ''
    form.cost = 0
  })
  .catch(error => console.error(error));
}

const onDeleteTransaction = async (transactionId) => {
  console.log(transactionId)
  fetch(`${import.meta.env.VITE_API_URL}/transactions/${transactionId}`, {
  method: 'DELETE',
  headers: {
    'Content-Type': 'application/json'
    }
  })
    .then(response => response.json())
    .then(data => {
      if (data === true) {
        // TODO: only update the fe state instead of pulling from be
        getTransaction() 
      }
    })
    .catch(error => console.error(error));
}
</script>

<template>
    <label>You ({{ state.currentUser }}) have paid: €{{ userPaid }}</label>
    <span v-for="debt in mappedDebt">
      <br>
      <label v-if="debt.from == state.currentUser">{{ debt.to }} owes you: €{{ debt.amount }}</label>
      <label v-else-if="debt.to == state.currentUser">you owe {{ debt.from }}: €{{ debt.amount }}</label>
    </span>
    <form @submit.prevent="save">
       <select v-model="form.email" required>
        <option v-for="user in state.trip.users" :value="user.email">{{ user.email }}</option>
       </select>
      <input type="text" placeholder="transaction name" v-model="form.title" required>
      <input type="number" min="0" placeholder='cost' v-model="form.cost">
      <div v-for="(user, index) in state.users">
        <label :for="'user-'+index">
          <span>{{ user.email }}</span>
          <input type="hidden" v-model="user.id">
          <input type="number" min="0" placeholder='cost' class="user-portion" v-model="user.cost">
        </label>
      </div>
      <button type="submit">Save</button>
    </form>
    <h4>List Transactions</h4>
    <TransactionItem
        v-for="transaction in state.transactions"
        :key="transaction.id"
        :transaction="transaction"
        @delete-transaction="onDeleteTransaction"
    ></TransactionItem>
</template>

<style>
.user-portion {
  display: inline-block;
}

pre {
  text-align: left;
  border-radius: 5%;
  padding: 1rem;
}
</style>