from typing import Optional

from typing import List
from typing import Optional

from pydantic import BaseModel, validator, ValidationError

class Alternativa(BaseModel):
    id: int
    texto: str
    possivel_causa_erro: str
    veracidade: bool
    id_questao: int
    id_proxima_questao: int

    class Config:
        orm_mode = True

class AlternativaCreate(Alternativa):
    pass

class Questao(BaseModel):
    id: int
    tema: str
    texto: str

    class Config:
        orm_mode = True

class QuestaoCreate(Questao):
    pass

class Aluno(BaseModel):
    id: int
    pilha_questoes: List
    lista_erros: List
    pilha_temas: List

class AlunoDB(BaseModel):
    id: int
    pilha_questoes: str
    lista_erros: str
    pilha_temas: str
    
    class Config:
        orm_mode = True
