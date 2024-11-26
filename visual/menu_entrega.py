from datetime import datetime, timedelta

from database.config import get_session
from models import cliente
from models.entrega import Entrega
from repository.banco_dados import BancoDados
from service.sistema_logistico import Logistica
from models.models import StatusEntrega


class MenuEntregas:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)
        self.logistica = Logistica()

    def menu_principal(self):
        while True:
            print("\n" + "=" * 60)
            print("               🚚 Menu de Entregas               ")
            print("=" * 60)
            print("1️⃣  Cadastrar Entrega")
            print("2️⃣  Despachar Entrega")
            print("3️⃣  Listar Alocações das Entregas")
            print("4️⃣  Finalizar Entrega")
            print("5️⃣  Cancelar Entrega")
            print("6️⃣  🔙 Voltar ao Menu Principal")
            print("=" * 60)
            opcao = input("🔹 Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_entrega()
            elif opcao == "2":
                self.colocar_entrega_em_rota()
            elif opcao == "3":
                self.exibir_alocacoes()
            elif opcao == "4":
                self.finalizar_entrega()
            elif opcao == "5":
                self.cancelar_entrega()
            elif opcao == "6":
                print("\n✅ Retornando ao menu principal...")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")

    def alocar_entregas(self):
        self.logistica.alocar_caminhoes()

    def cadastrar_entrega(self):
        print("\n    📦  Cadastrar Entrega  📦   ")

        try:
            peso = float(input("Digite o peso da entrega (em kg): "))
            volume = float(input("Digite o volume da entrega (m³): "))
            prazo_dias = int(input("Digite o prazo de entrega (em dias): "))
            prazo = datetime.now() + timedelta(days=prazo_dias)
        except ValueError:
            print("❌ Erro: Por favor, insira valores válidos para peso, volume ou prazo.")
            return

        clientes = self.banco_de_dados.listar_clientes()
        if not clientes:
            print("❌ Nenhum cliente cadastrado. Não é possível cadastrar a entrega.")
            return

        print("\n --- Clientes Disponíveis ---")
        print(f"{'ID':<5} | {'Nome':<30} | {'Endereço':<40} | {'Cidade/Estado':<20}")
        print("-" * 110)
        for cliente_cadastrado in clientes:
            print(f"{cliente_cadastrado.id:<5} | {cliente_cadastrado.nome:<30} | "
                  f"{cliente_cadastrado.endereco:<40} | {cliente_cadastrado.cidade}, {cliente_cadastrado.estado}")
        print("-" * 110)

        try:
            cliente_id = int(input("Digite o ID do cliente para a entrega: "))
            cliente = self.banco_de_dados.buscar_cliente_por_id(cliente_id)
            if not cliente:
                print(f"❌ Cliente com o ID '{cliente_id}' não encontrado no banco de dados.")
                return
        except ValueError:
            print("❌ Erro: Por favor, insira um ID válido.")
            return

        print("\n🔒 Confirme os dados antes de cadastrar a entrega:")
        print(f"\nEntrega:")
        print(f"Peso: {peso} kg")
        print(f"Volume: {volume} m³")
        print(f"Prazo de entrega: {prazo.strftime('%d/%m/%Y')}")

        print(f"\nCliente Selecionado:")
        print(f"Nome: {cliente.nome}")
        print(f"Endereço: {cliente.endereco}")
        print(f"Cidade/Estado: {cliente.cidade}, {cliente.estado}")

        confirmacao = input("\n✅ Confirmar cadastro? (S/N): ").strip().lower()

        if confirmacao != 's':
            print("\n❌ Cadastro cancelado.")
            return

        entrega = Entrega(
            peso=peso,
            volume=volume,
            prazo=prazo,
            endereco_entrega=cliente.endereco,
            cidade_entrega=cliente.cidade,
            estado_entrega=cliente.estado,
            latitude_entrega=cliente.latitude,
            longitude_entrega=cliente.longitude,
            cliente_id=cliente_id
        )

        try:
            self.session.add(entrega)
            self.session.commit()
            self.logistica.alocar_caminhoes()
            print("\n✅ Entrega cadastrada com sucesso!")
            print(
                f"\nID da Entrega: {entrega.id} | Peso: {entrega.peso} kg | Volume: {entrega.volume} m³ | Prazo: {prazo.strftime('%d/%m/%Y')}")
        except Exception as e:
            print(f"❌ Erro ao cadastrar a entrega: {e}")
            self.session.rollback()
        finally:
            self.session.close()

    def listar_entregas(self):
        print("\n    📦  Lista de Entregas  📦   ")
        entregas = self.session.query(Entrega).all()

        if not entregas:
            print("❌ Nenhuma entrega cadastrada.")
            return

        print(f"\n{'Código':<10} | {'Peso':<10} | {'Prazo':<15} | {'Status':<20}")
        print("-" * 65)

        for entrega in entregas:
            status = f"{entrega.status}".replace("StatusEntrega.", "").replace("_", " ").title()
            prazo = self.__formatar_data(f"{entrega.prazo}")
            print(f"{entrega.id:<10} | {entrega.peso:<10} kg | {prazo:<15} | {status:<20}")
        print("-" * 65)


    def colocar_entrega_em_rota(self):
        print("\n    📦  Atualizar Status da Entrega  📦   ")
        self.listar_entregas()

        try:
            id_entrega = int(input("\nSelecione o ID da entrega que deseja despachar: "))
        except ValueError:
            print("❌ ID inválido. Por favor, insira um número válido.")
            return

        entrega = self.session.query(Entrega).get(id_entrega)

        if not entrega:
            print("❌ Entrega não encontrada. Verifique o ID e tente novamente.")
            return

        if entrega.status == StatusEntrega.ENTREGUE:
            print("⚠️ A entrega já foi finalizada e não pode ser alterada.")
            return

        entrega.status = StatusEntrega.EM_ROTA
        self.session.commit()
        print(f"\n✅ Status da entrega {entrega.id} atualizado para 'Em Rota' com sucesso!")


    def cancelar_entrega(self):
        print("\n    ❌  Cancelar Entrega  ❌   ")
        self.listar_entregas()

        try:
            id_entrega = int(input("\nSelecione o ID da entrega que deseja cancelar: "))
        except ValueError:
            print("❌ ID inválido. Por favor, insira um número válido.")
            return

        entrega = self.banco_de_dados.buscar_entrega_por_id(id_entrega)

        if not entrega:
            print("❌ Entrega não encontrada. Verifique o ID e tente novamente.")
            return

        if entrega.status == StatusEntrega.ENTREGUE:
            print("⚠️ A entrega já foi finalizada e não pode ser cancelada.")
            return

        entrega.status = StatusEntrega.CANCELADA
        self.session.commit()
        print(f"\n✅ A entrega {entrega.id} foi cancelada com sucesso!")

    def exibir_alocacoes(self):
        rotas = self.banco_de_dados.listar_rotas()

        if not rotas:
            print("❌ Não há entregas alocadas para exibir.")
            return

        print("\n    --- 🚚 Entregas Alocadas 🚚 ---")

        for rota in rotas:
            caminhao = self.banco_de_dados.buscar_caminhao_por_id(rota.caminhao_id)
            centro_distribuicao = self.banco_de_dados.buscar_centro_por_id(caminhao.centro_distribuicao_id)
            entrega = self.banco_de_dados.buscar_entrega_por_id(rota.entrega_id)
            status = f"{entrega.status}".replace("StatusEntrega.", "").replace("_", " ").title()
            prazo = entrega.prazo.strftime("%d/%m/%Y %H:%M")

            print("\n" + "=" * 70)
            print(f"🚛 ID da Entrega: {rota.entrega_id}")
            print("-" * 70)
            print(f"📍 Centro Responsável: {centro_distribuicao.nome}")
            print(f"🚛 Caminhão Alocado: {caminhao.modelo} - {caminhao.placa}")
            print(f"🛣️ Distância Total: {rota.distancia_total:.2f} km")
            print(f"💰 Custo Total: R$ {rota.custo_total:.2f}")
            print(f"📅 Prazo de Entrega: {prazo}")
            print(f"📦 Status da Entrega: {status}")
            print("=" * 70)

    def finalizar_entrega(self):
        self.listar_entregas()

        try:
            id = int(input("Selecione a entrega que deseja finalizar (ID): "))
        except ValueError:
            print("⚠️ Erro: ID inválido. Por favor, insira um número.")
            return

        entrega = self.banco_de_dados.buscar_entrega_por_id(id)

        if not entrega:
            print(f"❌ Entrega com ID '{id}' não encontrada.")
            return

        if entrega.status == StatusEntrega.ENTREGUE:
            print("✅ A entrega já foi finalizada.")
            return

        entrega.status = StatusEntrega.ENTREGUE
        rota = self.banco_de_dados.buscar_rota_por_id(entrega.rota_id)

        if rota:
            rota.data_fim = datetime.now()
            self.session.commit()
            print(f"✅ Entrega {id} finalizada com sucesso!")
            print(f"    Caminhão: {rota.caminhao.modelo} - {rota.caminhao.placa}")
            print(f"    Data de conclusão: {rota.data_fim.strftime('%d/%m/%Y %H:%M')}")
        else:
            print("❌ Não foi possível encontrar a rota associada a esta entrega.")


    @staticmethod
    def __formatar_data(string_data: str) -> str:
        date_object = datetime.strptime(string_data, "%Y-%m-%d %H:%M:%S.%f")
        return date_object.strftime("%d/%m/%Y %H:%M")

