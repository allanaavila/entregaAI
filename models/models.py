from sqlalchemy import Column, Integer, ForeignKey, Table, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatusEntrega(enum.Enum):
    PENDENTE = "pendente"
    ALOCADA = "alocada"
    EM_ROTA = "em_rota"
    ENTREGUE = "entregue"
    CANCELADA = "cancelada"

entrega_rota = Table(
    'entrega_rota',
    Base.metadata,
    Column('entrega_id', Integer, ForeignKey('entregas.id'), primary_key=True),
    Column('rota_id', Integer, ForeignKey('rotas.id'), primary_key=True),
    UniqueConstraint('entrega_id', 'rota_id', name='uix_entrega_rota')
)
