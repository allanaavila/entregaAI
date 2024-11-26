from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime

from sqlalchemy.orm import relationship

from models.models import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True)
    endereco = Column(String(200))
    cidade = Column(String(100))
    estado = Column(String(2))
    latitude = Column(Float)
    longitude = Column(Float)

    entregas = relationship("Entrega", back_populates="cliente")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

from models.entrega import Entrega
