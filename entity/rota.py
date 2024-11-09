import heapq


class RotaGrafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_rota(self, origem, destino, distancia):
        if origem not in self.grafo:
            self.grafo[origem] = []
        if destino not in self.grafo:
            self.grafo[destino] = []
        self.grafo[origem].append((destino, distancia))
        self.grafo[destino].append((origem, distancia))

    def rota_mais_curta(self, inicio, destino):
        distancias = {nodo: float('inf') for nodo in self.grafo}
        distancias[inicio] = 0
        heap = [(0, inicio)]

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

    def __repr__(self):
        return f"RotaGrafo(grafo={self.grafo})"
