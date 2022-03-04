import queue
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import crud, models, schemas
from .database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Rotas

#Rota para criação de questão
@app.post("/questao/", response_model=schemas.Questao)
async def create_questao(questao: schemas.QuestaoCreate, db: Session = Depends(get_db)):
    db_questao = crud.create_questao(db, questao=questao)
    return db_questao

#Rota para consulta das questões
@app.get("/questoes/", response_model=List[schemas.Questao])
async def read_questoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questoes = crud.get_questoes(db, skip=skip, limit=limit)
    return questoes

#Rota para consulta de uma questão
@app.get("/questao/{questao_id}", response_model=schemas.Questao)
async def read_questao(questao_id: int, db: Session = Depends(get_db)):
    db_questao = crud.get_questao(db, questao_id=questao_id)
    if db_questao is None:
        raise HTTPException(status_code=404, detail="Questao não encontrada")
    return db_questao

#Rota para criação de alternativa
@app.post("/alternativa/", response_model=schemas.Alternativa)
async def create_alternativa(alternativa: schemas.AlternativaCreate, db: Session = Depends(get_db)):
    db_alternativa = crud.create_alternativa(db, alternativa=alternativa)
    return db_alternativa

#Rota para consulta das alternativas
@app.get("/alternativas/", response_model=List[schemas.Alternativa])
async def read_alternativas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alternativas = crud.get_alternativas(db, skip=skip, limit=limit)
    return alternativas

#Rota para consulta de uma alternativa
@app.get("/alternativa/{alternativa_id}", response_model=schemas.Alternativa)
async def read_alternativa(alternativa_id: int, db: Session = Depends(get_db)):
    db_alternativa = crud.get_alternativa(db, alternativa_id=alternativa_id)
    if db_alternativa is None:
        raise HTTPException(status_code=404, detail="Alternativa não encontrada")
    return db_alternativa

#Rota para criação de aluno
@app.post("/aluno/", response_model=schemas.AlunoDB)
async def create_aluno(aluno: schemas.Aluno, db: Session = Depends(get_db)):
    db_aluno = crud.create_aluno(db, aluno=aluno)
    return db_aluno

#Rota para consulta dos alunos
@app.get("/alunos/", response_model=List[schemas.AlunoDB])
async def read_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    alunos = crud.get_alunos(db, skip=skip, limit=limit)
    return alunos

#Rota para consulta de um aluno
@app.get("/aluno/{aluno_id}", response_model=schemas.AlunoDB)
async def read_aluno(aluno_id: int, db: Session = Depends(get_db)):
    db_aluno = crud.get_aluno(db, aluno_id=aluno_id)
    if db_aluno is None:
        raise HTTPException(status_code=404, detail="Aluno não encontrada")
    return db_aluno

#Rota para consulta de questão através do tema
@app.get("/tema/{tema}", response_model=schemas.Questao)
async def read_questao_tema(tema: str, db: Session = Depends(get_db)):
    questao = crud.get_questao_tema(db, tema=tema)
    return questao

#Rota para consulta das alternativas de uma questão
@app.get("/alternativas/questao/{questao_id}", response_model=List[schemas.Alternativa])
async def read_alternativas(questao_id: int, db: Session = Depends(get_db)):
    alternativas = crud.get_alternativas_questao(db, questao_id=questao_id)
    return alternativas

#Rota para retornar uma questão e suas alternativas
@app.get("/exame/{questao_id}")
async def exame(questao_id: int, aluno: schemas.Aluno = schemas.Aluno(), db: Session = Depends(get_db)):
    if aluno.id == 0:
        ultimo_id = crud.get_last_id_aluno(db)
        aluno.id = ultimo_id.id + 1
    questao = crud.get_questao(db, questao_id=questao_id)
    alternativas = crud.get_alternativas_questao(db, questao_id=questao_id)
    return aluno.id