import networkx as nx
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import os

from database.config import get_session
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega

class CalcularDistancia:
    def __init__(self):
        self.__user_agent = os.getenv("NOMINATIM_USER_AGENT", "default_user_agent")
        self.geolocator = Nominatim(user_agent=self.__user_agent)
        self.grafo = nx.Graph()


    def calcular_distancia(self, coordenadas_partida: tuple, coordenadas_entrega: tuple) -> float | None:
        """
        Calcula a distância entre dois pontos geográficos em quilômetros
        :param coordenadas_partida: Formato de entrada:(latitude, longitude) Latitude e Longitude do Centro de Saída da Entrega
        :type coordenadas_partida: tuple
        :param coordenadas_entrega: Formato de entrada:(latitude, longitude) Latitude e Longitude do Endereço de Entrega
        :type coordenadas_entrega: tuple
        :return:
        """
        latitude_inicial, longitude_inicial = coordenadas_partida
        latitude_final, longitude_final = coordenadas_entrega

        if None in [latitude_inicial, longitude_inicial, latitude_final, longitude_final]:
            return

        distancia = geodesic((latitude_inicial, longitude_inicial), (latitude_final, longitude_final)).kilometers
        return distancia

    def construir_grafo(self, centros_distribuicao, destinos):
        for nome, endereco in centros_distribuicao.items():
            self.adicionar_no_grafo(nome, endereco)

        for nome, endereco in destinos.items():
            self.adicionar_no_grafo(nome, endereco)

        for centro, endereco_centro in centros_distribuicao.items():
            for destino, endereco_destino in destinos.items():
                dist = self.calcular_distancia(endereco_centro, endereco_destino)
                if dist:
                    self.grafo.add_edge(centro, destino, weight=dist)

    def adicionar_no_grafo(self, nome, endereco):
        latitude, longitude = self.obter_coordenadas(endereco)
        if latitude is not None and longitude is not None:
            self.grafo.add_node(nome, pos=(latitude, longitude))


    def encontrar_rota_mais_curta(self, origem, destino):
        try:
            caminho = nx.dijkstra_path(self.grafo, origem, destino, weight='weight')
            custo_total = nx.dijkstra_path_length(self.grafo, origem, destino, weight='weight')
            return caminho, custo_total
        except nx.NetworkXNoPath:
            print(f"Não há caminho entre {origem} e {destino}")
            return None, None

    def calcular_menor_rota(self):
        session = get_session()
        centros_distribuicao = {cd.codigo: cd.endereco for cd in session.query(CentroDistribuicao).all()}

        entregas = {entrega.codigo: entrega.endereco_entrega for entrega in session.query(Entrega).all()}

        calculadora = CalcularDistancia()

        calculadora.construir_grafo(centros_distribuicao, entregas)

        for entrega_codigo, destino in entregas.items():
            melhor_rota = None
            melhor_distancia = float('inf')

            for centro_codigo, centro_endereco in centros_distribuicao.items():
                caminho, distancia = calculadora.encontrar_rota_mais_curta(centro_codigo, entrega_codigo)
                if distancia is not None and distancia < melhor_distancia:
                    melhor_distancia = distancia
                    melhor_rota = centro_codigo

            if melhor_rota:
                print(f"\n🔍 **Resultado da Busca pela Melhor Rota para Entrega {entrega_codigo}**")
                print(f"{'=' * 70}")
                print(f"🚚 **Centro de Distribuição Selecionado:** {melhor_rota}")
                print(f"📍 **Endereço do Centro:** {centros_distribuicao[melhor_rota]}")
                print(f"🛣️ **Distância até a entrega:** {melhor_distancia:.2f} km")
                print(f"{'=' * 70}")
            else:
                print(f"\n⚠️ **Nenhuma rota válida encontrada para a entrega {entrega_codigo}.**")
        session.close()

    def atualizar_grafo(self, centros_distribuicao, destinos):
        self.grafo.clear()
        self.construir_grafo(centros_distribuicao, destinos)
