
from entity.centro_distribuicao import CentroDistribuicao
from entity.caminhao import Caminhao
from repository.banco_dados import BancoDados


def main():
    # Criando a instância do banco de dados
    banco_dados = BancoDados()

    # Criando 4 centros de distribuição
    centro1 = CentroDistribuicao(nome="São Paulo")
    centro2 = CentroDistribuicao(nome="Rio de Janeiro")
    centro3 = CentroDistribuicao(nome="Belo Horizonte")
    centro4 = CentroDistribuicao(nome="Curitiba")

    # Salvando os centros de distribuição no banco de dados
    banco_dados.salvar_centro(centro1)
    banco_dados.salvar_centro(centro2)
    banco_dados.salvar_centro(centro3)
    banco_dados.salvar_centro(centro4)

    # Criando caminhões para cada centro de distribuição
    caminhao1 = Caminhao(id="C001", capacidade_maxima=10000, horas_operacao=80, carga_atual=2000, centro=centro1)
    caminhao2 = Caminhao(id="C002", capacidade_maxima=15000, horas_operacao=70, carga_atual=5000, centro=centro2)
    caminhao3 = Caminhao(id="C003", capacidade_maxima=8000, horas_operacao=60, carga_atual=1500, centro=centro3)
    caminhao4 = Caminhao(id="C004", capacidade_maxima=12000, horas_operacao=90, carga_atual=3000, centro=centro4)

    # Salvando os caminhões no banco de dados
    banco_dados.salvar_caminhao(caminhao1, centro1.nome)
    banco_dados.salvar_caminhao(caminhao2, centro2.nome)
    banco_dados.salvar_caminhao(caminhao3, centro3.nome)
    banco_dados.salvar_caminhao(caminhao4, centro4.nome)

    # Listando todos os caminhões
    print("\nLista de caminhões cadastrados:")
    caminhoes = banco_dados.listar_caminhoes()
    for caminhao in caminhoes:
        print(f"ID: {caminhao.id}, Capacidade: {caminhao.capacidade_maxima}, Centro: {caminhao.centro.nome}")

    # Buscando caminhões disponíveis com capacidade mínima necessária
    capacidade_necessaria = 9000
    print(f"\nCaminhões disponíveis para uma carga de {capacidade_necessaria} kg:")
    caminhoneiros_disponiveis = banco_dados.buscar_caminhao_disponivel(capacidade_necessaria)
    for caminhao in caminhoneiros_disponiveis:
        print(f"ID: {caminhao.id}, Capacidade: {caminhao.capacidade_maxima}, Centro: {caminhao.centro.nome}")

    # Fechar a conexão com o banco de dados
    banco_dados.fechar_conexao()

if __name__ == "__main__":
    main()
