# Urunan
### _Split your bills_

[![Build Status](https://github.com/rezpaditya/Urunan/actions/workflows/docker-deploy.yml/badge.svg)](https://github.com/rezpaditya/Urunan/actions)

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
- [ ] Report logic
- [ ] Auth0 integration

### Frontend
- [ ] Login page
- [ ] Trip page
- [ ] Transaction page
- [ ] Report page
- [ ] Auth0 integration

### CI/CD
- [x] Setup server
- [x] Github action
- [x] Containerize backend
- [x] Deploy backend
- [x] Containerize frontend
- [x] Deploy frontend
- [ ] Setup docker-compose
- [ ] Tests

#### Live demo: http://urunan.respa.id
#### Swagger API: http://urunan.respa.id:8080/docs
