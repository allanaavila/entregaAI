from sqlalchemy import Column, Integer, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatusEntrega(enum.Enum):
    PENDENTE = "pendente"
    ALOCADA = "alocada"
    EM_ROTA = "em_rota"
    ENTREGUE = "entregue"


class StatusCaminhao(enum.Enum):
    DISPONIVEL = "disponivel"
    EM_ROTA = "em_rota"
    MANUTENCAO = "manutencao"
    INATIVO = "inativo"

entrega_rota = Table(
    'entrega_rota',
    Base.metadata,
    Column('entrega_id', Integer, ForeignKey('entregas.id')),
    Column('rota_id', Integer, ForeignKey('rotas.id'))
)