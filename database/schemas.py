from typing import Optional

from typing import List
from typing import Optional

from pydantic import BaseModel, validator, ValidationError

class Alternativa(BaseModel):
    id: int
    tema: str
    texto: str
    possivel_causa_erro: str
    veracidade: bool
    id_questao: int

    class Config:
        orm_mode = True

class AlternativaCreate(Alternativa):
    pass

class Questao(BaseModel):
    id: int
    tema: str
    texto: str
    nivel: int

    class Config:
        orm_mode = True

class QuestaoCreate(Questao):
    pass

class Aluno(BaseModel):
    id: int = 0
    pilha_questoes: List = []
    pilha_temas: List = []
    lista_erros: List = []
    questoes_feitas: List = []
    temas_feitos: List = []

class AlunoDB(BaseModel):
    id: int
    pilha_questoes: str
    lista_erros: str
    pilha_temas: str
    questoes_feitas: str
    temas_feitos: str

    
    class Config:
        orm_mode = True
