from sys import exception

from database.config import get_session
from models.centro_distribuicao import CentroDistribuicao
from repository.banco_dados import BancoDados
from util.encontrar_localizacao import obter_coordenadas_opencage


class MenuCentrosDistribuicao:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def menu_principal(self):
        while True:
            print("\n" + "=" * 50)
            print("        🏢 Menu Centros de Distribuição       ")
            print("=" * 50)
            print("1️⃣  Listar Centros de Distribuição")
            print("2️⃣  Listar Caminhões por Centro de Distribuição")
            print("3️⃣  🔙 Voltar ao Menu Principal")
            print("=" * 50)
            opcao = input("🔹 Escolha uma opção: ")

            if opcao == "1":
                self.listar_centros()
            elif opcao == "2":
                self.listar_caminhoes_centro()
            elif opcao == "3":
                print("\n✅ Saindo do sistema... Até logo!")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")

    def listar_centros(self):
        print("\n--- Lista de Centros de Distribuição ---")
        centros = self.banco_de_dados.listar_centros()
        if not centros:
            print("Nenhum centro de distribuição cadastrado.")
        else:
            print("\nDetalhes dos Centros de Distribuição:")
            print(f"{'-' * 110}")
            print(
                f"{'ID':<5} | {'Código':<10} | {'Nome':<35} | {'Cidade':<20} | {'Estado':<5} | {'Capacidade Máxima':<15}")
            print(f"{'-' * 110}")
            for centro in centros:
                print(
                    f"{centro.id:<5} | {centro.codigo:<10} | {centro.nome:<35} | {centro.cidade:<20} | {centro.estado:<5} | {centro.capacidade_maxima:<15} kg")
                print(f"{'-' * 110}")

    def listar_caminhoes_centro(self):
        print("\n--- Listar Caminhões por Centro de Distribuição ---")
        centros = self.banco_de_dados.listar_centros()
        if not centros:
            print("Nenhum centro de distribuição cadastrado.")

        print("\nCentros de Distribuição:")
        print(f"{'-' * 80}")
        print(f"{'ID':<5} | {'Nome do Centro':<35} | {'Cidade':<20} | {'Estado':<2}")
        print(f"{'-' * 80}")
        for id, centro in enumerate(centros, start=1):
            print(f"{id:<5} | {centro.nome:<35} | {centro.cidade:<20} | {centro.estado:<2}")
        print(f"{'-' * 80}")

        try:
            opcao = int(input("\nEscolha o número do centro para listar os caminhões: "))
            if opcao < 1 or opcao > len(centros):
                print("Opção inválida. Tente novamente.")
                return

            centro_escolhido = centros[opcao - 1]

            caminhoes = self.banco_de_dados.listar_caminhoes_por_centro(centro_escolhido.id)
            if not caminhoes:
                print(f"Nenhum caminhão cadastrado para o centro {centro_escolhido.nome}.")
            else:
                print(f"\n{'-' * 10} Caminhões do {centro_escolhido.nome} {'-' * 10} \n")
                print(f"{'ID':^7} | {'Modelo':^30} | {'Placa':^12}")
                print("=" * 70)
                for caminhao in caminhoes:
                    print(f"{caminhao.id:^7} | {caminhao.modelo:^30} | {caminhao.placa:^12}")
                print("=" * 70)


        except ValueError:
            print("Entrada inválida. Digite o número correspondente ao centro.")