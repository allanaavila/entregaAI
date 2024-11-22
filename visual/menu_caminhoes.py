
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
        print("\n    🚛  Cadastrar Caminhão  🚛   ")

        placa = input("Digite a placa do caminhão: ")
        modelo = input("Digite o modelo do caminhão: ")
        capacidade = float(input("Digite a capacidade do caminhão (em kg): "))
        velocidade_media = float(input("Digite a velocidade média do caminhão (km/h): "))
        custo_km = float(input("Digite o custo por km do caminhão: "))

        centros_distribuicao = self.banco_de_dados.listar_centros()
        if not centros_distribuicao:
            print("\n❌ Nenhum centro de distribuição cadastrado. Não é possível cadastrar o caminhão.")
            return

        print("\nEscolha o Centro de Distribuição para o caminhão:")
        print(f"{'-' * 110}")
        print(f"{'ID':<5} | {'Código':<10} | {'Nome':<35} | {'Cidade':<20} | {'Estado':<5} | {'Capacidade Máxima':<15}")
        print(f"{'-' * 110}")
        for centro in centros_distribuicao:
            print(
                f"{centro.id:<5} | {centro.codigo:<10} | {centro.nome:<35} | {centro.cidade:<20} | {centro.estado:<5} | {centro.capacidade_maxima:<15} kg")
            print(f"{'-' * 110}")

        try:
            centro_id = int(input("Escolha o centro de distribuição para o caminhão (ID): "))

            centro_selecionado = self.banco_de_dados.buscar_centro_por_id(centro_id)
            if not centro_selecionado:
                print(f"\n❌ Centro com o ID '{centro_id}' não encontrado. Cadastro cancelado.")
                return

            print("\n🔒 Confirme os dados antes de cadastrar:")
            print(f"\nCaminhão:")
            print(f"Placa: {placa}")
            print(f"Modelo: {modelo}")
            print(f"Capacidade: {capacidade} kg")
            print(f"Velocidade Média: {velocidade_media} km/h")
            print(f"Custo por Km: R$ {custo_km:.2f}")

            print("\nCentro de Distribuição Selecionado:")
            print(f"Nome: {centro_selecionado.nome}")
            print(f"Cidade: {centro_selecionado.cidade}")
            print(f"Estado: {centro_selecionado.estado}")
            print(f"Capacidade Máxima: {centro_selecionado.capacidade_maxima} kg")

            confirmacao = input("\n✅ Confirmar cadastro? (S/N): ").strip().lower()

            if confirmacao != 's':
                print("\n❌ Cadastro cancelado.")
                return

            caminhao = Caminhao(
                placa=placa,
                modelo=modelo,
                capacidade=capacidade,
                velocidade_media=velocidade_media,
                custo_km=custo_km,
                centro_distribuicao_id=centro_selecionado.id
            )

            try:
                self.session.add(caminhao)
                self.session.commit()
                print("\n✅ Caminhão cadastrado com sucesso!")
                print(f"ID do Caminhão: {caminhao.id} | Modelo: {caminhao.modelo} | Placa: {caminhao.placa}")
            except Exception as e:
                print(f"\n❌ Erro ao cadastrar caminhão: {e}")
                self.session.rollback()

        except ValueError:
            print("❌ Erro: Digite um ID válido para o centro de distribuição.")
        finally:
            self.session.close()


    def listar_caminhoes(self):
        print("\n")
        print(" 🚛  Listagem dos Caminhões  🚛   \n")
        caminhoes = self.banco_de_dados.listar_caminhoes()

        if not caminhoes:
            print("Nenhum caminhão cadastrado.")
        else:
            print(
                f"{'ID':^6} | {'📍Placa':^10} | {'🚛 Modelo':^20} | {'📦 Capacidade':^12} | {'⏱️ Velocidade':^14} | {'💰 Custo/Km':^14} | {'🏢 Centro ID':^10}")
            print("=" * 115)

            for caminhao in caminhoes:
                print(
                    f"{caminhao.id:^6} | {caminhao.placa:^11} | {caminhao.modelo:^21} | {caminhao.capacidade:^13} | {caminhao.velocidade_media:^15} | R${caminhao.custo_km:^13} | {caminhao.centro_distribuicao_id:^11}"
                )
                print("=" * 115)

    def remover_caminhao(self):
        print("\n")
        print(" 🚛  Remover Caminhões  🚛   \n")
        caminhoes = self.banco_de_dados.listar_caminhoes()

        if not caminhoes:
            print("Nenhum caminhão cadastrado.")
            return

        print(
            f"{'ID':^6} | {'📍Placa':^10} | {'🚛 Modelo':^20} | {'📦 Capacidade':^12} | {'⏱️ Velocidade':^14} | {'💰 Custo/Km':^14} | {'🏢 Centro ID':^10}")
        print("=" * 115)

        for i, caminhao in enumerate(caminhoes, start=1):
            print(
                f"{caminhao.id:^6} | {caminhao.placa:^11} | {caminhao.modelo:^21} | {caminhao.capacidade:^13} | {caminhao.velocidade_media:^15} | R${caminhao.custo_km:^13.2f} | {caminhao.centro_distribuicao_id:^11}"
            )
            print("=" * 115)

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