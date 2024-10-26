FROM python:3.11.3-slim-buster

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
ENV PATH="/.venv/bin:$PATH"

RUN mkdir -p /data/urunan
WORKDIR /src
COPY . /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--ssl-keyfile=./app/key.pem", "--ssl-certfile=./app/cert.pem"]