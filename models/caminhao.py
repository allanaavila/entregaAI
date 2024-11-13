from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.models import Base, StatusCaminhao


class Caminhao(Base):
    __tablename__ = 'caminhoes'

    id = Column(Integer, primary_key=True)
    placa = Column(String(8), unique=True, nullable=False)
    modelo = Column(String(50))
    capacidade = Column(Float, nullable=False)  # em kg ou m³
    velocidade_media = Column(Float, nullable=False)  # km/h
    custo_km = Column(Float, nullable=False)
    status = Column(Enum(StatusCaminhao), default=StatusCaminhao.DISPONIVEL)

    # Relacionamentos
    centro_distribuicao_id = Column(Integer, ForeignKey('centros_distribuicao.id'))
    centro_distribuicao = relationship("CentroDistribuicao", back_populates="caminhoes")
    rotas = relationship("Rota", back_populates="caminhao")

    # Dados de manutenção
    ultima_manutencao = Column(DateTime)
    quilometragem_total = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())









