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


@app.post("/questao/", response_model=schemas.Questao)
async def create_questao(questao: schemas.QuestaoCreate, db: Session = Depends(get_db)):
    db_questao = crud.create_questao(db, questao=questao)
    return db_questao


@app.get("/questoes/", response_model=List[schemas.Questao])
async def read_questoes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    questoes = crud.get_questoes(db, skip=skip, limit=limit)
    return questoes


@app.get("/questoes/{questao_id}", response_model=schemas.Questao)
async def read_questao(questao_id: int, db: Session = Depends(get_db)):
    db_questao = crud.get_questao(db, questao_id=questao_id)
    if db_questao is None:
        raise HTTPException(status_code=404, detail="Questao not found")
    return db_questao
