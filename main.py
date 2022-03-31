from curses.ascii import alt
import queue
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from .database import crud, models, schemas
from .database.database import SessionLocal, engine
from .database.batch_loader import carrega_alternativas, carrega_questoes

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

@app.get("/carrega_batch")
async def carrega_batch(db: Session = Depends(get_db)):
    carrega_questoes(db)
    carrega_alternativas(db)

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
@app.post("/exame/{questao_id}/{alternativa_id}")
async def exame(questao_id: int, aluno: schemas.Aluno, db: Session = Depends(get_db), alternativa_id: int = 0):
    if aluno is None:
        aluno = schemas.Aluno
    #Primeira questão acessada
    if (alternativa_id == 0):
        proxima_questao = crud.get_questao(db, questao_id=questao_id)
        alternativas = crud.get_alternativas_questao(db, questao_id=questao_id)
    #Caso seja selecionado a opção de finalizar o exame
    elif (alternativa_id == 5):
        return aluno
    #Questão vindo de outra questão anterior
    else:
        alternativa_anterior = crud.get_alternativa(db, alternativa_id=alternativa_id)
        #Questao anterior        
        questao_anterior = crud.get_questao(db, alternativa_anterior.id_questao)
        #Extraindo tema da alternativa
        tema = alternativa_anterior.tema
        #Calculo de nivel
        if alternativa_anterior.tema == questao_anterior.tema:
            nivel = questao_anterior.nivel - 1
        else:
            nivel = 3
        #Consulta lista de possiveis questoes de mesmo tema e nivel
        proximas_questoes = crud.get_questoes_tema_nivel(db, tema=tema, nivel=nivel)
        contador = 0
        for questao in proximas_questoes:
            contador += 1
            #Escolhe uma questao que ainda nao foi feita pelo aluno
            if questao not in aluno.questoes_feitas:
                proxima_questao = questao
                break
            #Caso o aluno tenha feito todas as questoes buscadas
            #é verificado se há questao na pilha de questoes
            #caso não haja, retorna tela com resultado final
            if contador == len(proximas_questoes):
                if aluno.pilha_questoes is not None:
                    proxima_questao = aluno.pilha_questoes.pop()
                else:
                    return aluno
        #Caso a alternativa seja errada
        if not alternativa_anterior.veracidade:
            aluno.pilha_questoes.append(questao_anterior)
            aluno.lista_erros.append(alternativa_anterior.possivel_causa_erro)
            aluno.pilha_temas.append(questao_anterior.tema)
        #Caso a alternativa seja correta
        else:
            #Caso exista temas na pilha de temas
            if aluno.pilha_temas:
                # Caso o tema ja tenha acabado, retorna para a questão q causou a descida de nivel
                if proxima_questao.tema not in aluno.pilha_temas:
                    print("Tema desempilhado: " + aluno.pilha_temas.pop())
                    proxima_questao = aluno.pilha_questoes.pop()
        alternativas = crud.get_alternativas_questao(db, questao_id=proxima_questao.id)

        alternativa_nao_sei = schemas.Alternativa(id_questao = proxima_questao.id, veracidade = False,
                                        tema = proxima_questao.tema,texto = 'Não sei', id = 0,
                                        possivel_causa_erro = 'Conhecimento sobre o tema')
        alternativas.append(alternativa_nao_sei)
    return aluno, alternativas, proxima_questao