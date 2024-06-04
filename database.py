from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Substitua com suas credenciais do AWS RDS
DATABASE_URI = 'mysql+pymysql://admin:admin123@professores1.cngeuki48zub.us-east-1.rds.amazonaws.com:3306/professores1'

engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Eventual(Base):
    __tablename__ = 'eventuais'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    conta = Column(String)
    agencia = Column(String)
    banco = Column(String)

class Efetivo(Base):
    __tablename__ = 'efetivos'
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(String)
    nif = Column(String)
    especialidade = Column(String)

class AulaEventual(Base):
    __tablename__ = 'aulas_eventuais'
    id = Column(Integer, primary_key=True)
    eventual_id = Column(Integer, ForeignKey('eventuais.id'))
    efetivo_id = Column(Integer, ForeignKey('efetivos.id'))
    entrada = Column(DateTime)
    saida = Column(DateTime)
    quantidade_aulas = Column(Integer)
    observacoes = Column(String)

    eventual = relationship('Eventual')
    efetivo = relationship('Efetivo')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
