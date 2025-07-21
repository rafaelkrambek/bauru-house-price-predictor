from sqlalchemy import Column, Integer, Float, DateTime
from datetime import datetime
from database import Base

class Previsao(Base):
    __tablename__ = "previsoes"

    id = Column(Integer, primary_key=True, index=True)
    quartos = Column(Integer)
    banheiros = Column(Integer)
    vagas = Column(Integer)
    tamanhos = Column(Integer)
    preco_medio = Column(Float)
    preco_previsto = Column(Float)
    criado_em = Column(DateTime, default=datetime.utcnow)