# define base image
FROM python:3.8

COPY . .

RUN apt-get update

RUN pip install poetry

RUN poetry install

CMD ["poetry",  "run", "uvicorn",  "app.main:app",  "--host",  "0.0.0.0",  "--port",  "8000",  "--reload"]
