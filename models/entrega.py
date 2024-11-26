from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.models import Base, entrega_rota, StatusEntrega


class Entrega(Base):
    __tablename__ = 'entregas'

    id = Column(Integer, primary_key=True)
    peso = Column(Float, nullable=False)
    volume = Column(Float)
    prazo = Column(DateTime, nullable=False)
    prioridade = Column(Integer, default=0)
    status = Column(Enum(StatusEntrega), default=StatusEntrega.PENDENTE)

    endereco_entrega = Column(String(200), nullable=False)
    cidade_entrega = Column(String(100), nullable=False)
    estado_entrega = Column(String(2), nullable=False)
    latitude_entrega = Column(Float, nullable=False)
    longitude_entrega = Column(Float, nullable=False)

    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship("Cliente", back_populates="entregas")

    centro_distribuicao_id = Column(Integer, ForeignKey('centros_distribuicao.id'))
    centro_distribuicao = relationship("CentroDistribuicao", back_populates="entregas")

    rota_id = Column(Integer, ForeignKey('rotas.id'))
    rotas = relationship("Rota", secondary=entrega_rota, back_populates="entrega")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

from models.cliente import Cliente
from models.centro_distribuicao import CentroDistribuicao
from models.rota import Rota