from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Questao(Base):
    __tablename__ = "questoes"

    id = Column(Integer, primary_key=True, index=True)
    tema = Column(String, index=True)
    texto = Column(String, index=True)
    alternativa1 = Column(String, index=True)
    alternativa2 = Column(String, index=True)
    alternativa3 = Column(String, index=True)
    alternativa4 = Column(String, index=True)
    alternativa5 = Column(String, index=True)
    
    #email = Column(String, unique=True, index=True)
    #hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)

    #alternativas = relationship("Item", back_populates="owner")


class Alternativa(Base):
    __tablename__ = "alternativas"

    id = Column(Integer, primary_key=True, index=True)
    texto = Column(String, index=True)
    possivel_causa_erro = Column(String, index=True)
    veracidade = Column(Boolean, default=False)
    id_questao = Column(Integer, ForeignKey("questoes.id"))

    #owner = relationship("User", back_populates="items")