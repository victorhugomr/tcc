from sqlalchemy.orm import Session

from . import models, schemas


def get_questao(db: Session, questao_id: int):
    return db.query(models.Questao).filter(models.Questao.id == questao_id).first()


def get_questoes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Questao).offset(skip).limit(limit).all()


def create_questao(db: Session, questao: schemas.QuestaoCreate):
    db_questao = models.Questao(tema=questao.tema,texto=questao.texto,
                                alternativa1=questao.alternativa1, alternativa2= questao.alternativa2, 
                                alternativa3=questao.alternativa3, alternativa4=questao.alternativa4, 
                                alternativa5=questao.alternativa5)
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
                                veracidade=alternativa.veracidade, id_questao= alternativa.id_questao)
    db.add(db_alternativa)
    db.commit()
    db.refresh(db_alternativa)
    return db_alternativa

def get_aluno(db: Session, aluno_id: int):
    return db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()


def get_alunos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Aluno).offset(skip).limit(limit).all()


def create_aluno(db: Session, aluno: schemas.AlunoCreate):
    db_aluno = models.Aluno(pilha_questoes=aluno.pilha_questoes[0],lista_erros=aluno.lista_erros[0],
                                pilha_temas=aluno.pilha_temas[0])
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)
    return db_aluno