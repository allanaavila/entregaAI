# main.py
from datetime import datetime, timedelta
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import track

# Importar as classes do sistema
from otimizador import OtimizadorLogistica
from models import Entrega, Caminhao, StatusEntrega

console = Console()


def gerar_entregas_teste(quantidade: int) -> list:
    """Gera entregas aleatórias para teste"""
    cidades = [
        ("Manaus", "AM"), ("Salvador", "BA"), ("Fortaleza", "CE"),
        ("Brasília", "DF"), ("Vitória", "ES"), ("Goiânia", "GO"),
        ("São Luís", "MA"), ("Belo Horizonte", "MG"), ("João Pessoa", "PB"),
        ("Porto Alegre", "RS"), ("Florianópolis", "SC"), ("Aracaju", "SE"),
        ("Palmas", "TO"), ("Campo Grande", "MS"), ("Cuiabá", "MT")
    ]

    entregas = []
    for i in range(quantidade):
        cidade, estado = random.choice(cidades)
        peso = random.uniform(100, 1000)  # Entre 100kg e 1000kg
        prazo = datetime.now() + timedelta(days=random.randint(1, 5))

        entrega = Entrega(
            id=f"ENT-{i + 1:03d}",
            destino=f"{cidade}, {estado}",
            peso=round(peso, 2),
            prazo=prazo
        )
        entregas.append(entrega)

    return entregas


def criar_frota_teste() -> list:
    """Cria uma frota de teste com diferentes tipos de caminhões"""
    caminhoes = []

    # Configurações dos tipos de caminhões
    tipos_caminhao = [
        # (capacidade, velocidade, custo_km)
        (1500, 70, 2.5),  # Pequeno
        (2500, 65, 3.0),  # Médio
        (3500, 60, 3.5)  # Grande
    ]

    # Criar caminhões para cada CD
    cds = ["CD-BE", "CD-RE", "CD-SP", "CD-CW"]

    for cd in cds:
        for i, (capacidade, velocidade, custo) in enumerate(tipos_caminhao):
            caminhao = Caminhao(
                id=f"CAM-{cd[-2:]}-{i + 1:02d}",
                capacidade=capacidade,
                velocidade_media=velocidade,
                centro_distribuicao=cd,
                custo_km=custo
            )
            caminhoes.append(caminhao)

    return caminhoes


def mostrar_estatisticas_entrega(rotas_otimizadas: dict, entregas_originais: list):
    """Mostra estatísticas das entregas e rotas"""
    total_entregas = len(entregas_originais)
    entregas_alocadas = sum(len(rota) for rota in rotas_otimizadas.values())

    tabela = Table(title="Estatísticas de Entregas")
    tabela.add_column("Métrica", style="cyan")
    tabela.add_column("Valor", justify="right")

    tabela.add_row("Total de Entregas", str(total_entregas))
    tabela.add_row("Entregas Alocadas", str(entregas_alocadas))
    tabela.add_row("Taxa de Alocação", f"{(entregas_alocadas / total_entregas) * 100:.1f}%")

    console.print(Panel(tabela))


def mostrar_detalhes_rotas(rotas_otimizadas: dict, otimizador: OtimizadorLogistica):
    """Mostra detalhes de cada rota otimizada"""
    for caminhao_id, rota in rotas_otimizadas.items():
        if not rota:
            continue

        tabela = Table(title=f"Rota do Caminhão {caminhao_id}")
        tabela.add_column("Entrega")
        tabela.add_column("Destino")
        tabela.add_column("Peso (kg)")
        tabela.add_column("Prazo")
        tabela.add_column("CD")

        for entrega in rota:
            tabela.add_row(
                entrega.id,
                entrega.destino,
                f"{entrega.peso:.2f}",
                entrega.prazo.strftime("%d/%m/%Y %H:%M"),
                entrega.centro_distribuicao
            )

        console.print(tabela)
        console.print("")


def calcular_metricas_rota(rota: list, caminhao: Caminhao, otimizador: OtimizadorLogistica):
    """Calcula métricas importantes para uma rota"""
    if not rota:
        return 0, 0, 0

    distancia_total = 0
    peso_total = 0
    coords_atual = otimizador.centros_distribuicao[caminhao.centro_distribuicao]

    for entrega in rota:
        if not entrega.coordenadas:
            entrega.coordenadas = otimizador.obter_coordenadas(entrega.destino)

        if entrega.coordenadas:
            distancia = otimizador.calcular_distancia_ajustada(coords_atual, entrega.coordenadas)
            distancia_total += distancia
            coords_atual = entrega.coordenadas

        peso_total += entrega.peso

    custo_total = distancia_total * caminhao.custo_km

    return distancia_total, peso_total, custo_total


def mostrar_metricas_sistema(rotas_otimizadas: dict, caminhoes: list, otimizador: OtimizadorLogistica):
    """Mostra métricas gerais do sistema"""
    tabela = Table(title="Métricas do Sistema")
    tabela.add_column("Caminhão")
    tabela.add_column("Entregas")
    tabela.add_column("Distância (km)")
    tabela.add_column("Peso Total (kg)")
    tabela.add_column("Custo (R$)")
    tabela.add_column("Ocupação (%)")

    total_distancia = 0
    total_custo = 0

    for caminhao in caminhoes:
        rota = rotas_otimizadas.get(caminhao.id, [])
        distancia, peso, custo = calcular_metricas_rota(rota, caminhao, otimizador)
        ocupacao = (peso / caminhao.capacidade) * 100 if peso > 0 else 0

        total_distancia += distancia
        total_custo += custo

        tabela.add_row(
            caminhao.id,
            str(len(rota)),
            f"{distancia:.1f}",
            f"{peso:.1f}",
            f"R$ {custo:.2f}",
            f"{ocupacao:.1f}%"
        )

    console.print(tabela)
    console.print(f"\nDistância Total: {total_distancia:.1f} km")
    console.print(f"Custo Total: R$ {total_custo:.2f}")


def main():
    console.print("[bold green]Iniciando Sistema de Otimização Logística[/bold green]")

    # Inicializar o otimizador
    otimizador = OtimizadorLogistica()

    # Criar dados de teste
    num_entregas = 20
    console.print(f"\nGerando {num_entregas} entregas aleatórias...")
    entregas = gerar_entregas_teste(num_entregas)

    console.print("\nCriando frota de caminhões...")
    caminhoes = criar_frota_teste()

    # Executar otimização
    console.print("\n[bold]Otimizando rotas...[/bold]")
    with console.status("[bold green]Processando otimização...") as status:
        rotas_otimizadas = otimizador.otimizar_entregas(entregas, caminhoes)

    # Mostrar resultados
    console.print("\n[bold]Resultados da Otimização:[/bold]")
    mostrar_estatisticas_entrega(rotas_otimizadas, entregas)
    mostrar_detalhes_rotas(rotas_otimizadas, otimizador)
    mostrar_metricas_sistema(rotas_otimizadas, caminhoes, otimizador)


if __name__ == "__main__":
    main()




from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv
import os
from typing import List, Dict
from dataclasses import dataclass
from datetime import datetime, timedelta
import heapq


@dataclass
class Entrega:
    id: str
    destino: str
    peso: float
    prazo: datetime
    coordenadas: tuple = None


@dataclass
class Caminhao:
    id: str
    capacidade: float
    velocidade_media: float  # km/h
    centro_distribuicao: str
    entregas_designadas: List[Entrega] = None

    def __post_init__(self):
        self.entregas_designadas = []
        self.carga_atual = 0


class SistemaRotas:
    def __init__(self):
        load_dotenv(override=True)
        self.__user_agent = os.getenv("NOMINATIM_USER_AGENT")
        self.geolocator = Nominatim(user_agent=self.__user_agent)
        self.centros_distribuicao = {}  # Armazena coordenadas dos CDs

    def adicionar_centro_distribuicao(self, nome: str, endereco: str):
        """Adiciona um novo centro de distribuição ao sistema"""
        try:
            location = self.geolocator.geocode(endereco)
            self.centros_distribuicao[nome] = (location.latitude, location.longitude)
            return True
        except Exception as e:
            print(f"Erro ao adicionar CD: {str(e)}")
            return False

    def calcular_distancia(self, coord1: tuple, coord2: tuple) -> float:
        """Calcula distância entre dois pontos e aplica fator de custo"""
        distancia = geodesic(coord1, coord2).kilometers

        if distancia < 300:
            return distancia * 1.44
        elif 301 <= distancia <= 999:
            return distancia * 1.3
        else:
            return distancia * 1.4

    def obter_coordenadas(self, endereco: str) -> tuple:
        """Obtém coordenadas de um endereço"""
        try:
            location = self.geolocator.geocode(endereco)
            return (location.latitude, location.longitude)
        except Exception as e:
            print(f"Erro ao obter coordenadas: {str(e)}")
            return None

    def encontrar_cd_mais_proximo(self, entrega: Entrega) -> str:
        """Encontra o centro de distribuição mais próximo do destino"""
        if not entrega.coordenadas:
            entrega.coordenadas = self.obter_coordenadas(entrega.destino)

        cd_mais_proximo = None
        menor_distancia = float('inf')

        for nome_cd, coord_cd in self.centros_distribuicao.items():
            dist = self.calcular_distancia(coord_cd, entrega.coordenadas)
            if dist < menor_distancia:
                menor_distancia = dist
                cd_mais_proximo = nome_cd

        return cd_mais_proximo

    def otimizar_rotas(self, entregas: List[Entrega], caminhoes: List[Caminhao]) -> Dict:
        """Otimiza as rotas para todos os caminhões"""
        # Pré-processamento: associar entregas aos CDs mais próximos
        entregas_por_cd = {}
        for entrega in entregas:
            cd = self.encontrar_cd_mais_proximo(entrega)
            if cd not in entregas_por_cd:
                entregas_por_cd[cd] = []
            entregas_por_cd[cd].append(entrega)

        # Ordenar entregas por prazo em cada CD
        for cd in entregas_por_cd:
            entregas_por_cd[cd].sort(key=lambda x: x.prazo)

        # Associar caminhões aos CDs
        caminhoes_por_cd = {}
        for caminhao in caminhoes:
            if caminhao.centro_distribuicao not in caminhoes_por_cd:
                caminhoes_por_cd[caminhao.centro_distribuicao] = []
            caminhoes_por_cd[caminhao.centro_distribuicao].append(caminhao)

        rotas_otimizadas = {}

        # Para cada CD, alocar entregas aos caminhões
        for cd, entregas_cd in entregas_por_cd.items():
            if cd not in caminhoes_por_cd:
                print(f"Aviso: Não há caminhões disponíveis no CD {cd}")
                continue

            caminhoes_disponiveis = caminhoes_por_cd[cd]

            # Algoritmo guloso para alocação de entregas
            for entrega in entregas_cd:
                alocada = False
                for caminhao in caminhoes_disponiveis:
                    if (caminhao.carga_atual + entrega.peso <= caminhao.capacidade and
                            self.verificar_viabilidade_tempo(caminhao, entrega)):
                        caminhao.entregas_designadas.append(entrega)
                        caminhao.carga_atual += entrega.peso
                        alocada = True
                        break

                if not alocada:
                    print(f"Aviso: Não foi possível alocar entrega {entrega.id}")

            # Otimizar sequência de entregas para cada caminhão
            for caminhao in caminhoes_disponiveis:
                if caminhao.entregas_designadas:
                    self.otimizar_sequencia_entregas(caminhao)
                    rotas_otimizadas[caminhao.id] = caminhao.entregas_designadas

        return rotas_otimizadas

    def verificar_viabilidade_tempo(self, caminhao: Caminhao, nova_entrega: Entrega) -> bool:
        """Verifica se é possível adicionar nova entrega respeitando prazos"""
        coord_cd = self.centros_distribuicao[caminhao.centro_distribuicao]
        tempo_atual = datetime.now()

        # Simular rota com nova entrega
        entregas_simuladas = caminhao.entregas_designadas + [nova_entrega]

        posicao_atual = coord_cd
        for entrega in entregas_simuladas:
            distancia = self.calcular_distancia(posicao_atual, entrega.coordenadas)
            tempo_viagem = distancia / caminhao.velocidade_media  # em horas
            tempo_atual += timedelta(hours=tempo_viagem)

            if tempo_atual > entrega.prazo:
                return False

            posicao_atual = entrega.coordenadas

        return True

    def otimizar_sequencia_entregas(self, caminhao: Caminhao):
        """Otimiza a sequência de entregas usando algoritmo do vizinho mais próximo"""
        if not caminhao.entregas_designadas:
            return

        coord_cd = self.centros_distribuicao[caminhao.centro_distribuicao]
        entregas_ordenadas = []
        entregas_restantes = caminhao.entregas_designadas.copy()

        posicao_atual = coord_cd

        while entregas_restantes:
            proxima_entrega = None
            menor_distancia = float('inf')

            for entrega in entregas_restantes:
                dist = self.calcular_distancia(posicao_atual, entrega.coordenadas)
                if dist < menor_distancia:
                    menor_distancia = dist
                    proxima_entrega = entrega

            if proxima_entrega:
                entregas_ordenadas.append(proxima_entrega)
                entregas_restantes.remove(proxima_entrega)
                posicao_atual = proxima_entrega.coordenadas

        caminhao.entregas_designadas = entregas_ordenadas


# Exemplo de uso
def exemplo_uso():
    # Inicializar sistema
    sistema = SistemaRotas()

    # Adicionar centros de distribuição
    sistema.adicionar_centro_distribuicao("CD-SP", "São Paulo, SP")
    sistema.adicionar_centro_distribuicao("CD-RJ", "Rio de Janeiro, RJ")

    # Criar entregas
    entregas = [
        Entrega("E1", "Campinas, SP", 500, datetime.now() + timedelta(days=1)),
        Entrega("E2", "Santos, SP", 300, datetime.now() + timedelta(days=1)),
        Entrega("E3", "Niterói, RJ", 400, datetime.now() + timedelta(days=2))
    ]

    # Criar caminhões
    caminhoes = [
        Caminhao("C1", 1000, 60, "CD-SP"),
        Caminhao("C2", 1500, 55, "CD-RJ")
    ]

    # Otimizar rotas
    rotas = sistema.otimizar_rotas(entregas, caminhoes)

    # Imprimir resultados
    for caminhao_id, entregas in rotas.items():
        print(f"\nRotas para caminhão {caminhao_id}:")
        for entrega in entregas:
            print(f"  - Entrega {entrega.id} para {entrega.destino}")


if __name__ == "__main__":
    exemplo_uso()