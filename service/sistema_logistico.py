from database.init_db import logger


class Logistica:
    def __init__(self, centros, caminhoes, entregas, calculadora_distancia):
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
            melhor_distancia = float('inf')
            caminhao_alocado = None

            for centro in self.centros:
                distancia = self.calculadora_distancia.calcular_distancia(centro.endereco, entrega.endereco_entrega)
                if distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = centro

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
            if caminhao.centro_distribuicao == centro and caminhao.capacidade >= peso and caminhao.pode_transportar(peso):
                return caminhao
        return None

    def exibir_alocacao(self, alocacao):
        for entrega, caminhao in alocacao.items():
            print(
                f"Entrega {entrega.id} alocada ao caminhão {caminhao.id} ({caminhao.centro_distribuicao.nome}) com peso {entrega.peso}kg.")

