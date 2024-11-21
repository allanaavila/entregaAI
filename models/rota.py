from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship

from models.models import Base, entrega_rota, StatusEntrega


class Rota(Base):
    __tablename__ = 'rotas'

    id = Column(Integer, primary_key=True)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime)
    distancia_total = Column(Float, nullable=False)
    custo_total = Column(Float, nullable=False)

    caminhao_id = Column(Integer, ForeignKey('caminhoes.id'), nullable=False)
    caminhao = relationship("Caminhao", back_populates="rotas")

    entrega_id = Column(Integer, ForeignKey('entregas.id'), nullable=False)
    entrega = relationship("Entrega", secondary=entrega_rota, back_populates="rotas")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

from models.caminhao import Caminhao
from models.entrega import Entrega