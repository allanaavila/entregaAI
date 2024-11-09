from repository.banco_dados import BancoDados
from service.sistema_logistico import SistemaLogistico
from entity.centro_distribuicao import CentroDistribuicao
from entity.caminhao import Caminhao
from entity.entrega import Entrega

def main():
    banco_dados = BancoDados()

    # Inicializar o sistema logístico
    sistema = SistemaLogistico(banco_dados)

    # Criar e adicionar centros de distribuição
    cd_sao_paulo = CentroDistribuicao("Centro de Distribuição de São Paulo")
    cd_recife = CentroDistribuicao("Centro de Distribuição de Recife")
    cd_belem = CentroDistribuicao("Centro de Distribuição de Belém")
    cd_curitiba = CentroDistribuicao("Centro de Distribuição de Curitiba")

    sistema.adicionar_centro_distribuicao(cd_sao_paulo)
    sistema.adicionar_centro_distribuicao(cd_recife)
    sistema.adicionar_centro_distribuicao(cd_belem)
    sistema.adicionar_centro_distribuicao(cd_curitiba)

    # Criar e adicionar caminhões aos centros de distribuição
    caminhao_sp = Caminhao("SP001", 10000, 8)
    caminhao_pa = Caminhao("SP002", 10000, 8)
    caminhao_pe = Caminhao("SP003", 10000, 8)
    caminhao_pr = Caminhao("SP004", 10000, 8)

    sistema.adicionar_caminhao(caminhao_sp, "Centro de Distribuição de São Paulo")
    sistema.adicionar_caminhao(caminhao_pa, "Centro de Distribuição de Belém")
    sistema.adicionar_caminhao(caminhao_pe, "Centro de Distribuição de Recife")
    sistema.adicionar_caminhao(caminhao_pr, "Centro de Distribuição de Curitiba")

    # Criar e adicionar rotas entre os centros de distribuição
    sistema.adicionar_rota("Centro de Distribuição de São Paulo", "Centro de Distribuição de Curitiba", 400)
    sistema.adicionar_rota("Centro de Distribuição de Curitiba", "Centro de Distribuição de Belém", 500)
    sistema.adicionar_rota("Centro de Distribuição de Curitiba", "Centro de Distribuição de Recife", 750)

    # Criar entrega e alocar para um centro de distribuição
    entrega_curitiba = Entrega("Centro de Distribuição de Curitiba", "2024-12-15", 500)
    sistema.alocar_entrega("Centro de Distribuição de São Paulo", entrega_curitiba)

    banco_dados.fechar_conexao()

if __name__ == "__main__":
    main()
