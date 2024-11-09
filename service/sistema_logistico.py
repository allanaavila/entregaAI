from repository.banco_dados import BancoDados
from repository.caminhao_repository import CaminhaoRepository
from repository.centro_distribuicao_repository import CentroDistribuicaoRepository
from entity.rota import RotaGrafo

class SistemaLogistico:
    def __init__(self, banco_dados):
        self.centro_repositorio = CentroDistribuicaoRepository(banco_dados)
        self.caminhao_repositorio = CaminhaoRepository(banco_dados)
        self.grafo_rotas = RotaGrafo()

    def adicionar_centro_distribuicao(self, centro):
        self.centro_repositorio.salvar(centro)

    def adicionar_caminhao(self, caminhao, centro_nome):
        centro = self.centro_repositorio.buscar(centro_nome)
        if centro:
            centro.adicionar_caminhao(caminhao)
            self.caminhao_repositorio.salvar(caminhao, centro_nome)

    def adicionar_rota(self, origem, destino, distancia):
        self.grafo_rotas.adicionar_rota(origem, destino, distancia)

    def alocar_entrega(self, centro_nome, entrega):
        centro = self.centro_repositorio.buscar(centro_nome)
        if centro:
            caminhao = self._selecionar_caminhao(centro, entrega.peso)
            if caminhao:
                distancia = self.grafo_rotas.rota_mais_curta(centro_nome, entrega.destino)
                if distancia:
                    print(
                        f"Entrega (Destino: {entrega.destino}, Prazo: {entrega.prazo_entrega}, Peso: {entrega.peso} kg) "
                        f"alocada ao caminhão {caminhao.id}.\n"
                        f"Rota: {centro_nome} -> {entrega.destino}, Distância: {distancia} km."
                    )
                else:
                    print(f"Não foi possível encontrar uma rota para o destino {entrega.destino}.")
            else:
                print("Nenhum caminhão disponível com capacidade para a entrega.")
        else:
            print(f"Centro de distribuição {centro_nome} não encontrado.")

    def _selecionar_caminhao(self, centro, peso_entrega):
        for caminhao in centro.caminhoes:
            if caminhao.pode_carregar(peso_entrega):
                caminhao.carga_atual += peso_entrega
                return caminhao
        return None
