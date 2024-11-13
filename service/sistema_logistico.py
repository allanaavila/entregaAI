import logging


class Logistica:
    def __init__(self, centros, caminhoes, entregas, grafo):
        if not centros or not caminhoes or not entregas or not grafo:
            raise ValueError("Centros, caminhões, entregas e grafo são necessários.")

        self.centros = centros
        self.caminhoes = caminhoes
        self.entregas = entregas
        self.grafo = grafo

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def alocar_caminhoes(self):
        alocacao = {}

        for entrega in self.entregas:
            melhor_rota = None
            melhor_distancia = float('inf')
            caminhao_alocado = None

            for centro in self.centros:
                distancia = self.grafo.rota_mais_curta(centro, entrega.destino)
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = centro

            caminhao = self.encontrar_caminhao_adequado(melhor_rota, entrega.peso)
            if caminhao:
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

    def calcular_rota_ideal(self, origem, destino):
        rota = self.grafo.rotas.get((origem, destino))
        if rota is None:
            self.logger.warning(f"Rota de {origem} para {destino} não encontrada.")
        return rota

    def exibir_alocacao(self, alocacao):
        for entrega, caminhao in alocacao.items():
            print(f"Entrega {entrega.id} alocada ao caminhão {caminhao.id} ({caminhao.centro_distribuicao.nome}).")
