import json
import os
from sqlalchemy.orm import Session
from .schemas import Questao, Alternativa
from .crud import create_alternativa, create_questao

def carrega_questoes(db: Session):
    # Abre arquivo JSON
    f = open('app/questoes.json')

    # retorna o objeto JSON como
    # um dictionary
    questoes = json.load(f)

    # itera sob o json
    for questao in questoes:
        modelo_questao = Questao(id = questao['id'], nivel = questao['nivel'],
                                tema = questao['tema'], texto = questao['texto'])
        create_questao(db, modelo_questao)

    # Fecha o arquivo
    f.close()

def carrega_alternativas(db: Session):
    # Abre arquivo JSON
    f = open('app/alternativas.json')

    # retorna o objeto JSON como
    # um dictionary
    alternativas = json.load(f)

    # itera sob o json
    for alternativa in alternativas:
        modelo_alternativa = Alternativa(id_questao = alternativa['id_questao'], veracidade = alternativa['veracidade'],
                                        tema = alternativa['tema'],texto = alternativa['texto'], id = 0,
                                        possivel_causa_erro = alternativa['possivel_causa_erro'])
        
        create_alternativa(db, modelo_alternativa)

    # Fecha o arquivo
    f.close()