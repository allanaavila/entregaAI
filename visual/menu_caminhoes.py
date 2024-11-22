
from database.config import get_session
from models.caminhao import Caminhao
from repository.banco_dados import BancoDados, ErroBancoDados


class MenuCaminhoes:

    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def exibir_menu(self):
        while True:
            print("\n" + "=" * 40)
            print("          🚛 Menu de Caminhões 🚛         ")
            print("=" * 40)
            print("1️⃣  Cadastrar Caminhão")
            print("2️⃣  Listar Caminhões")
            print("3️⃣  Remover Caminhão")
            print("4️⃣  Voltar ao menu principal")
            print("=" * 40)
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_caminhao()
            elif opcao == "2":
                self.listar_caminhoes()
            elif opcao == "3":
                self.remover_caminhao()
            elif opcao == "4":
                print("\n✅ Retornando ao menu principal...")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")

    def cadastrar_caminhao(self):
        print("\n--- Cadastrar Caminhão ---")
        placa = input("Digite a placa do caminhão: ")
        modelo = input("Digite o modelo do caminhão: ")
        capacidade = float(input("Digite a capacidade do caminhão (em kg): "))
        velocidade_media = float(input("Digite a velocidade média do caminhão (km/h): "))
        custo_km = float(input("Digite o custo por km do caminhão: "))

        centros_distribuicao = self.banco_de_dados.listar_centros()
        print("\nCentros de Distribuição disponíveis:")
        for centro in centros_distribuicao:
            print(f"{centro.id}. {centro.nome} - {centro.cidade}, {centro.estado}")
        centro_id = int(input("Escolha o centro de distribuição para o caminhão (número): "))

        centro_selecionado = self.banco_de_dados.buscar_centro_por_id(centro_id)

        if not centro_selecionado:
            print(f"Centro com o id '{centro_id}' não encontrado no banco de dados.")

        caminhao = Caminhao(
            placa=placa,
            modelo=modelo,
            capacidade=capacidade,
            velocidade_media=velocidade_media,
            custo_km=custo_km,
            centro_distribuicao_id=centro_id
        )

        self.session.add(caminhao)
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


    def remover_caminhao(self):
        print("\n--- Remover Caminhão ---")

        caminhoes = self.banco_de_dados.listar_caminhoes()

        if not caminhoes:
            print("Nenhum caminhão cadastrado.")
            return

        for i, caminhao in enumerate(caminhoes, start=1):
            print(
                f"{i}. ID: {caminhao.id} - Modelo: {caminhao.modelo} - Placa: {caminhao.placa}, Capacidade: {caminhao.capacidade} kg")

        caminhao_id = input("Digite o ID do caminhão a ser removido: ").strip()

        caminhao_remover = next((caminhao for caminhao in caminhoes if str(caminhao.id) == caminhao_id), None)

        if not caminhao_remover:
            print(f"Nenhum caminhão encontrado com o ID {caminhao_id}.")
            return

        try:
            self.banco_de_dados.remover_caminhao(caminhao_id)
            print(f"Caminhão com ID {caminhao_id} removido com sucesso!")
        except ErroBancoDados as e:
            print(f"Erro ao remover caminhão: {str(e)}")

    def __del__(self):
        self.session.close()