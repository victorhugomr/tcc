from fastapi import FastAPI
from models import Questao, Alternativa, Aluno

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}