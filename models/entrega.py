from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship

from models.models import Base, entrega_rota, StatusEntrega


class Entrega(Base):
    __tablename__ = 'entregas'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(20), unique=True, nullable=False)
    peso = Column(Float, nullable=False)
    volume = Column(Float)
    prazo = Column(DateTime, nullable=False)
    prioridade = Column(Integer, default=0)
    status = Column(Enum(StatusEntrega), default=StatusEntrega.PENDENTE)

    endereco_entrega = Column(String(200), nullable=False)
    cidade_entrega = Column(String(100), nullable=False)
    estado_entrega = Column(String(2), nullable=False)
    latitude_entrega = Column(Float)
    longitude_entrega = Column(Float)

    cliente_id = Column(Integer, ForeignKey('clientes.id'))
    cliente = relationship("Cliente", back_populates="entregas")

    centro_distribuicao_id = Column(Integer, ForeignKey('centros_distribuicao.id'))
    centro_distribuicao = relationship("CentroDistribuicao", back_populates="entregas")

    rotas = relationship("Rota", secondary=entrega_rota, back_populates="entregas")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())