from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from models.models import Base


class CentroDistribuicao(Base):
    __tablename__ = 'centros_distribuicao'

    id = Column(Integer, primary_key=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nome = Column(String(100), nullable=False)
    endereco = Column(String(200), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    capacidade_maxima = Column(Float)

    caminhoes = relationship("Caminhao", back_populates="centro_distribuicao")
    entregas = relationship("Entrega", back_populates="centro_distribuicao")

    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    def tem_caminhao_disponivel(self, peso: float) -> bool:
        if len(self.caminhoes) == 0 or not self.caminhoes:
            return False
        else:
            tem_caminhao_disponivel = False
            for caminhao in self.caminhoes:
                if caminhao.pode_transportar(peso):
                    tem_caminhao_disponivel = True
                    break
            return tem_caminhao_disponivel



from models.caminhao import Caminhao
from models.entrega import Entrega
