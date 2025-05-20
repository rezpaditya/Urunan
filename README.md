# Urunan
### _Split your bills_

[![Build Status](https://github.com/rezpaditya/Urunan/actions/workflows/docker-deploy.yml/badge.svg)](https://github.com/rezpaditya/Urunan/actions)

![image](https://github.com/user-attachments/assets/ac23ee49-98e4-4d3e-9392-499a1f587cec)


### Development setup
```sh
cd backend
pipenv install
uvicorn run backend.main:app --reload

cd frontend
npm install
npm run dev
```

### Backend
- [x] Trip CRUD
- [x] Trans CRUD
- [x] Report logic
- [x] Auth0 integration

### Frontend
- [x] Login page
- [x] Trip page
- [x] Transaction page
- [x] Report page
- [x] Auth0 integration

### CI/CD
- [x] Setup server
- [x] Github action
- [x] Containerize backend
- [x] Deploy backend
- [x] Containerize frontend
- [x] Deploy frontend
- [ ] Setup docker-compose
- [ ] E2E Tests

#### Live demo: https://urunan.respa.id
#### Swagger API: https://urunan.respa.id:8080/docs
