from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Eventual(Base):
    __tablename__ = 'eventuais'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    conta = Column(String, nullable=False)
    agencia = Column(String, nullable=False)
    banco = Column(String, nullable=False)

    aulas = relationship('AulaEventual', back_populates='eventual')

class Efetivo(Base):
    __tablename__ = 'efetivos'

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, unique=True, nullable=False)
    nif = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)

    aulas = relationship('AulaEventual', back_populates='efetivo')

class AulaEventual(Base):
    __tablename__ = 'aulas_eventuais'

    id = Column(Integer, primary_key=True, index=True)
    eventual_id = Column(Integer, ForeignKey('eventuais.id'), nullable=False)
    efetivo_id = Column(Integer, ForeignKey('efetivos.id'), nullable=False)
    horario_entrada = Column(String, nullable=False)
    horario_saida = Column(String, nullable=False)
    quantidade_aulas = Column(Integer, nullable=False)
    observacoes = Column(String, nullable=True)

    eventual = relationship('Eventual', back_populates='aulas')
    efetivo = relationship('Efetivo', back_populates='aulas')
