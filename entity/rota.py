import heapq

from entity.distancia import Distancia


class RotaGrafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_rota(self, origem, destino, lat1, lon1, lat2, lon2):
        distancia_obj = Distancia(lat1, lon1, lat2, lon2)
        distancia = distancia_obj.calcular_distancia()

        if origem not in self.grafo:
            self.grafo[origem] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origem].append((destino, distancia))
        self.grafo[destino].append((origem, distancia))

    def rota_mais_curta(self, origem, destino):
        if origem not in self.grafo or destino not in self.grafo:
            raise ValueError(f"Origem ou Destino não encontrados no grafo: {origem}, {destino}")

        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[origem] = 0
        heap = [(0, origem)]

        # Algoritmo de Dijkstra para encontrar o menor caminho
        while heap:
            distancia_atual, nodo_atual = heapq.heappop(heap)

            if nodo_atual == destino:
                return distancia_atual

            if distancia_atual > distancias[nodo_atual]:
                continue

            for vizinho, peso in self.grafo[nodo_atual]:
                distancia = distancia_atual + peso
                if distancia < distancias[vizinho]:
                    distancias[vizinho] = distancia
                    heapq.heappush(heap, (distancia, vizinho))

        return distancias[destino] if distancias[destino] != float('inf') else None
