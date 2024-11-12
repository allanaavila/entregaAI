class Logistica:
    def __init__(self, centros, caminhoes, entregas, grafo):
        self.centros = centros
        self.caminhoes = caminhoes
        self.entregas = entregas
        self.grafo = grafo

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

            for caminhao in self.caminhoes:
                if caminhao.centro_distribuicao == melhor_rota and caminhao.pode_transportar(entrega.peso):
                    caminhao.adicionar_carga(entrega.peso)
                    alocacao[entrega] = caminhao
                    break

        return alocacao

    def encontrar_caminhao_adequado(self, centro, peso):
        for caminhao in self.caminhoes:
            if caminhao.centro_distribuicao == centro and caminhao.capacidade >= peso:
                return caminhao
        return None

    def calcular_rota_ideal(self, origem, destino):
        return self.grafo.rotas.get((origem, destino), None)
