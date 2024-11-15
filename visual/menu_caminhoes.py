
from database.config import get_session
from models.caminhao import Caminhao
from repository.banco_dados import BancoDados



class MenuCaminhoes:

    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def exibir_menu(self):
        while True:
            print("\n--- Menu de Caminhões ---")
            print("1. Cadastrar Caminhão")
            print("2. Listar Caminhões")
            print("3. Voltar ao Menu Principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_caminhao()
            elif opcao == "2":
                self.listar_caminhoes()
            elif opcao == "3":
                break
            else:
                print("Opção inválida! Tente novamente.")

    def cadastrar_caminhao(self):
        print("\n--- Cadastrar Caminhão ---")
        placa = input("Digite a placa do caminhão: ")
        modelo = input("Digite o modelo do caminhão: ")
        capacidade = float(input("Digite a capacidade do caminhão (em kg): "))
        velocidade_media = float(input("Digite a velocidade média do caminhão (km/h): "))
        custo_km = float(input("Digite o custo por km do caminhão: "))

        centros_distribuicao = self.banco_de_dados.listar_centros()
        print("\nCentros de Distribuição disponíveis:")
        for i, centro in enumerate(centros_distribuicao, start=1):
            print(f"{i}. {centro.nome} - {centro.cidade}, {centro.estado}")
        centro_id = int(input("Escolha o centro de distribuição para o caminhão (número): "))

        centro_selecionado = centros_distribuicao[centro_id - 1]

        caminhao = Caminhao(
            placa=placa,
            modelo=modelo,
            capacidade=capacidade,
            velocidade_media=velocidade_media,
            custo_km=custo_km,
            centro_distribuicao_id=centro_selecionado.id
        )

        self.session.add_all(caminhao)
        self.session.commit()
        print("Caminhão cadastrado com sucesso!")
        self.session.close()

    def listar_caminhoes(self):
        print("\n--- Listar Caminhões ---")
        caminhoes = self.banco_de_dados.listar_caminhoes()

        if not caminhoes:
            print("Nenhum caminhão cadastrado.")
        else:
            for caminhao in caminhoes:
                print(f"ID: {caminhao.id}, Placa: {caminhao.placa}, Modelo: {caminhao.modelo}, "
                      f"Capacidade: {caminhao.capacidade} kg, Velocidade Média: {caminhao.velocidade_media} km/h, "
                      f"Custo por Km: R${caminhao.custo_km}, Centro de Distribuição ID: {caminhao.centro_distribuicao_id}")

    def __del__(self):
        self.session.close()