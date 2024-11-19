from database.config import get_session
from database.init_db import logger
from typing import List, Type

from models.caminhao import Caminhao
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega
from util.calcular_distancia import CalcularDistancia


class Logistica:
    alocacoes = []

    def __init__(self):
        self.session = get_session()
        self.centros = self.session.query(CentroDistribuicao).all()
        self.caminhoes = self.session.query(Caminhao).all()
        self.entregas = self.session.query(Entrega).all()
        self.calculadora_distancia = CalcularDistancia()
        self.logger = logger

    def alocar_caminhoes(self):
        """
        Realiza a alocação das entregas para os caminhões mais adequados.
        """
        if not self.centros or not self.caminhoes or not self.entregas:
            self.logger.warning("Dados insuficientes para realizar a alocação.")
            return

        for entrega in self.entregas:
            melhor_rota = None
            melhor_distancia = float('inf')

            for centro in self.centros:
                distancia = self.calculadora_distancia.calcular_distancia(
                    (centro.latitude, centro.longitude),
                    (entrega.latitude_entrega, entrega.longitude_entrega)
                )
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = centro

            if not melhor_rota:
                self.logger.warning(f"Nenhum centro adequado encontrado para a entrega {entrega.id}.")
                continue

            caminhao = self.encontrar_caminhao_adequado(melhor_rota, entrega.peso)
            if not caminhao:
                self.logger.warning(f"Nenhum caminhão disponível no centro {melhor_rota.nome} para a entrega {entrega.id}.")
                continue

            if caminhao.capacidade - caminhao.carga_atual < entrega.peso:
                self.logger.warning(
                    f"Capacidade insuficiente no caminhão {caminhao.id} para a entrega {entrega.id}."
                )
                continue

            caminhao.adicionar_carga(entrega.peso)
            Logistica.alocacoes.append((entrega, caminhao, melhor_rota))
            self.logger.info(f"Caminhão {caminhao.id} alocado para a entrega {entrega.id}.")

    def encontrar_caminhao_adequado(self, centro, peso):
        """
        Retorna o caminhão mais adequado para uma entrega específica em um centro de distribuição.
        """
        return next(
            (caminhao for caminhao in self.caminhoes if caminhao.centro_distribuicao_id == centro.id and caminhao.capacidade >= peso),
            None
        )

    @staticmethod
    def exibir_alocacao():
        if not Logistica.alocacoes:
            print("Nenhuma alocação realizada.")
            return

        for entrega, caminhao, centro in Logistica.alocacoes:
            print(
                f"\n--- Alocação ---"
                f"\nCentro de Distribuição: {centro.nome} ({centro.cidade}, {centro.estado})"
                f"\nCaminhão: {caminhao.modelo} - Placa: {caminhao.placa}, Capacidade: {caminhao.capacidade}kg"
                f"\nEntrega: ID {entrega.id}, Peso: {entrega.peso}kg, Volume: {entrega.volume}, "
                f"Prazo: {entrega.prazo.strftime('%Y-%m-%d %H:%M')}"
                f"\nDestino: {entrega.endereco_entrega}, {entrega.cidade_entrega}, {entrega.estado_entrega}\n"
            )
