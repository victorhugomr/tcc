from sqlalchemy.orm import Session
from typing import List

from . import models, schemas

def trata_dados_aluno(lista: List):
    texto_saida = ""
    for elemento in lista:
        texto_saida += elemento+", "
    size = len(texto_saida)
    texto_saida = texto_saida[:size - 2]
    return texto_saida

def get_questao(db: Session, questao_id: int):
    return db.query(models.Questao).filter(models.Questao.id == questao_id).first()


def get_questoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Questao).offset(skip).limit(limit).all()


def create_questao(db: Session, questao: schemas.QuestaoCreate):
    db_questao = models.Questao(tema=questao.tema,texto=questao.texto)
    db.add(db_questao)
    db.commit()
    db.refresh(db_questao)
    return db_questao

def get_alternativa(db: Session, alternativa_id: int):
    return db.query(models.Alternativa).filter(models.Alternativa.id == alternativa_id).first()


def get_alternativas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Alternativa).offset(skip).limit(limit).all()


def create_alternativa(db: Session, alternativa: schemas.AlternativaCreate):
    db_alternativa = models.Alternativa(texto=alternativa.texto,possivel_causa_erro=alternativa.possivel_causa_erro,
                                veracidade=alternativa.veracidade, id_questao= alternativa.id_questao, id_proxima_questao= alternativa.id_proxima_questao)
    db.add(db_alternativa)
    db.commit()
    db.refresh(db_alternativa)
    return db_alternativa

def get_aluno(db: Session, aluno_id: int):
    return db.query(models.AlunoDB).filter(models.AlunoDB.id == aluno_id).first()


def get_alunos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AlunoDB).offset(skip).limit(limit).all()


def create_aluno(db: Session, aluno: schemas.Aluno):
    db_aluno = models.AlunoDB(pilha_questoes=trata_dados_aluno(aluno.pilha_questoes),
                            lista_erros=trata_dados_aluno(aluno.lista_erros),
                            pilha_temas=trata_dados_aluno(aluno.pilha_temas))
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno