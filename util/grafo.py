import sys

class Grafo:
    def __init__(self):
        self.grafo = {}

    def adicionar_aresta(self, u, v, peso):
        if u not in self.grafo:
            self.grafo[u] = {}
        if v not in self.grafo:
            self.grafo[v] = {}
        self.grafo[u][v] = peso
        self.grafo[v][u] = peso

    def dijkstra(self, origem):
        distancias = {v: sys.maxsize for v in self.grafo}
        distancias[origem] = 0
        caminho = {v: None for v in self.grafo}
        visitado = {v: False for v in self.grafo}

        for _ in range(len(self.grafo)):
            u = min((v for v in distancias if not visitado[v]), key=distancias.get)
            visitado[u] = True

            for vizinho, peso in self.grafo[u].items():
                if not visitado[vizinho] and distancias[u] + peso < distancias[vizinho]:
                    distancias[vizinho] = distancias[u] + peso
                    caminho[vizinho] = u

        return distancias, caminho
