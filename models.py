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

    class Config:
        orm_mode = True

class Questao(BaseModel):
    id: int
    alternativa1: int
    alternativa2: int
    alternativa3: int
    alternativa4: int
    alternativa5: int

    class Config:
        orm_mode = True

class Aluno(BaseModel):
    id: int
    pilha_questoes: List
    lista_erros: List
    pilha_temas: List