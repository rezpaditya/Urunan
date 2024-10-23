
<script setup>
import { reactive, onMounted, computed, watch } from 'vue'
import TransactionItem from '../components/TransactionItem.vue'
import { useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'


const userStore = useUserStore()
const route = useRoute()
const tripId = route.params.id;

const state = reactive({
    trip: {},
    transactions: [],
    users: [],
    currentUser: '',
    resolvedDebt: [],
    isSubmitDisabled: false
})

const form = reactive({
  email: '',
  title: '',
  cost: 0,
  details: []
})

watch(form, () => {
  state.trip.users.map(user => {
    user['cost'] = parseFloat((form.cost / state.trip.users.length).toFixed(2))
  }),
  {deep: true}
})

watch(state, () => {
  const total = state.users.reduce((total, user) => total + user.cost, 0)
  state.isSubmitDisabled = (total > form.cost),
  {deep: true}
})

onMounted(() => {
  getTransaction()
  state.currentUser = userStore.user.email
  console.log('user store value is: ', userStore.user)
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
                      from_user: borrower,
                      to_user: lender,
                      amount: amountOwed
                  });
                  userDebt[borrower] -= amountOwed;
                  userDebt[lender] += amountOwed;
              }
          }
      });
  });
  state.resolvedDebt = mappedDebt.map(debt => {
    return {
      trip_id: tripId,
      from_user: debt.from_user.id,
      to_user: debt.to_user.id,
      amount: debt.amount
    }
  })
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

const resolve = async () => {
  fetch(`${import.meta.env.VITE_API_URL}/trips/resolve/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      trip_id: tripId,
      debts: state.resolvedDebt
    })
  })
  .then(response => response.json())
  .then(data => {
    getTransaction()
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
    <div v-if="!state.trip.is_resolved" class="my-4">
      <div class="my-10">
        <h1 class="my-5 text-xl">🗒️ Transaction Summary</h1>
        <label>You ({{ userStore.user.given_name }}) have paid: €{{ userPaid }}</label>
        <span v-for="debt in mappedDebt">
          <br>
          <label v-if="debt.from_user.email == state.currentUser">{{ debt.to_user.email }} owes you: €{{ debt.amount }}</label>
          <label v-else-if="debt.to_user.email == state.currentUser">you owe {{ debt.from_user.email }}: €{{ debt.amount }}</label>
        </span>
        <br>
        <button @click="resolve" class="p-1 px-3 rounded-md text-white bg-blue-400 inline-block text-sm">Settle Trip</button>
      </div>
      
      <h1 class="my-5 text-xl">🥤 Add Transaction</h1>
      <form @submit.prevent="save">
        <label class="text-xs">Select Payer</label>
        <select v-model="form.email" required class="p-2 block w-full border border-slate-200 dark:bg-white rounded-md">
          <option v-for="user in state.trip.users" :value="user.email">{{ user.email }}</option>
        </select>
        <input type="text" placeholder="transaction name" v-model="form.title" required class="p-2 block w-full border border-slate-200 rounded-md">
        <div class="relative">
          <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
            €
          </div>
          <input type="number" min="0" step="any" placeholder="cost" v-model="form.cost" class="ps-10 p-2.5 block w-full border border-slate-200 rounded-md">
        </div>
        
        <h1 class="my-5 text-xl mt-10 mb-4">⚖️ User Portions</h1>
        <div v-for="(user, index) in state.users" class="form">
          <label class="text-xs">{{ user.email }}</label>
          <div class="relative">
            <div class="absolute inset-y-0 start-0 flex items-center ps-3.5 pointer-events-none">
              €
            </div>
            <input type="number" min="0" step="any" placeholder="cost" v-model="user.cost" class="text-sm block w-full ps-10 p-2.5 border border-slate-200 rounded-md" >
          </div>

          <input type="hidden" v-model="user.id">
        </div>
        <label v-if="state.isSubmitDisabled" class="text-red-500">⚠️ Total portion cannot exceed<br> the transaction cost!</label>
        <button type="submit" :disabled="state.isSubmitDisabled" :class="state.isSubmitDisabled ? 'cursor-not-allowed opacity-50': ''" class="p-2 rounded-md text-white bg-teal-500 w-full">Save</button>
      </form>
    </div>
    <div v-else>
      <label>This trip has been settled!</label>
      <h1 class="my-5 text-xl">Expense Summary</h1>
      <div v-for="debt in mappedDebt">
        <label>{{ debt.to_user.email }} owes {{ debt.from_user.email }}: €{{ debt.amount }}</label>
      </div>
    </div>
    <br>
    <br>
    <h1 class="my-5 text-xl mb-2">List Transactions</h1>
    <TransactionItem
        v-for="transaction in state.transactions"
        :key="transaction.id"
        :transaction="transaction"
        :isTripSettled="state.trip.is_resolved"
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

.form {
  text-align: left;
}
</style>