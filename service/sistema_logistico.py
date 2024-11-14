from database.init_db import logger
from typing import List, Type

from models.caminhao import Caminhao
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega
from util.calcular_distancia import CalcularDistancia


class Logistica:
    def __init__(self, centros: List[Type[CentroDistribuicao]], caminhoes: List[Type[Caminhao]], entregas: List[Type[Entrega]],
                 calculadora_distancia: CalcularDistancia = CalcularDistancia()):
        if not centros or not caminhoes or not entregas:
            raise ValueError("Centros, caminhões e entregas são necessários.")
        self.centros = centros
        self.caminhoes = caminhoes
        self.entregas = entregas
        self.calculadora_distancia = calculadora_distancia
        self.logger = logger

    def alocar_caminhoes(self):
        alocacao = {}

        for entrega in self.entregas:
            melhor_rota = None
            melhor_distancia = None

            for indice, centro in enumerate(self.centros, start=1):
                distancia = self.calculadora_distancia.calcular_distancia(
                    (centro.latitude, centro.longitude),
                    (entrega.latitude_entrega, entrega.longitude_entrega)
                )

                if indice == 1:
                    melhor_distancia = distancia
                    melhor_rota = centro
                    continue

                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = centro

            if not melhor_rota:
                self.logger.warning(f"Nenhuma rota encontrada para a entrega {entrega.id}.")
                continue

            caminhao = self.encontrar_caminhao_adequado(melhor_rota, entrega.peso)

            if caminhao:
                if caminhao.capacidade - caminhao.carga_atual < entrega.peso:
                    self.logger.warning(
                        f"Não há capacidade suficiente no caminhão {caminhao.id} para a entrega {entrega.id}.")
                    continue

                caminhao.adicionar_carga(entrega.peso)
                alocacao[entrega] = caminhao
                self.logger.info(f"Caminhão {caminhao.id} alocado para a entrega {entrega.id}.")
            else:
                self.logger.warning(
                    f"Não há caminhão adequado para a entrega {entrega.id} no centro {melhor_rota.nome}.")

        return alocacao

    def encontrar_caminhao_adequado(self, centro, peso):
        for caminhao in self.caminhoes:
            if caminhao.centro_distribuicao == centro and caminhao.capacidade >= peso and caminhao.pode_transportar(
                    peso):
                return caminhao
        return None

    def exibir_alocacao(self, alocacao):
        for entrega, caminhao in alocacao.items():
            centro = caminhao.centro_distribuicao
            print(
                f"\n--- Alocação de Entrega ---"
                f"\nCentro de Distribuição: {centro.nome} ({centro.cidade}, {centro.estado})"
                f"\nCaminhão: ID {caminhao.id}, Placa: {caminhao.placa}, Modelo: {caminhao.modelo}, Capacidade: {caminhao.capacidade}kg"
                f"\nEntrega: ID {entrega.id}, Peso: {entrega.peso}kg, Volume: {entrega.volume},"
                f"\n   Destino: {entrega.endereco_entrega}, {entrega.cidade_entrega} - {entrega.estado_entrega}"
                f"\n   Prazo: {entrega.prazo.strftime('%Y-%m-%d %H:%M')}\n"
            )

