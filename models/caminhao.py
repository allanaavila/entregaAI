from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.models import Base, StatusCaminhao


class Caminhao(Base):
    __tablename__ = 'caminhoes'

    id = Column(Integer, primary_key=True)
    placa = Column(String(8), unique=True, nullable=False)
    modelo = Column(String(50))
    capacidade = Column(Float, nullable=False)
    velocidade_media = Column(Float, nullable=False)
    custo_km = Column(Float, nullable=False)
    status = Column(Enum(StatusCaminhao), default=StatusCaminhao.DISPONIVEL)

    #
    centro_distribuicao_id = Column(Integer, ForeignKey('centros_distribuicao.id'))
    centro_distribuicao = relationship("CentroDistribuicao", back_populates="caminhoes")
    rotas = relationship("Rota", back_populates="caminhao")

    ultima_manutencao = Column(DateTime)
    quilometragem_total = Column(Float, default=0)

    carga_atual = Column(Float, default=0)

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def pode_transportar(self, peso):
        return self.capacidade - self.carga_atual >= peso

    def adicionar_carga(self, peso):
        if self.pode_transportar(peso):
            self.carga_atual += peso
        else:
            raise ValueError(f"O caminhão {self.placa} não tem capacidade suficiente para essa carga.")










