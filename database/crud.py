from sqlalchemy.orm import Session

from . import models, schemas


def get_questao(db: Session, questao_id: int):
    return db.query(models.Questao).filter(models.Questao.id == questao_id).first()


def get_questoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Questao).offset(skip).limit(limit).all()


def create_questao(db: Session, questao: schemas.QuestaoCreate):
    db_questao = models.Questao(alternativa1=questao.alternativa1, alternativa2= questao.alternativa2, 
                                alternativa3=questao.alternativa3, alternativa4=questao.alternativa4, 
                                alternativa5=questao.alternativa5)
    db.add(db_questao)
    db.commit()
    db.refresh(db_questao)
    return db_questao