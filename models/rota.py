from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from models.models import Base, entrega_rota


class Rota(Base):
    __tablename__ = 'rotas'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    data_inicio = Column(DateTime)
    data_fim = Column(DateTime)
    distancia_total = Column(Float)  # em km
    custo_total = Column(Float)
    status = Column(String(20))

    # Relacionamentos
    caminhao_id = Column(Integer, ForeignKey('caminhoes.id'))
    caminhao = relationship("Caminhao", back_populates="rotas")

    entregas = relationship("Entrega", secondary=entrega_rota, back_populates="rotas")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())