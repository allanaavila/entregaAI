from datetime import datetime, timedelta

from database.config import get_session
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
            print("\n--- Menu de Entregas ---")
            print("1. Cadastrar Entrega")
            print("2. Alocar Entregas")
            print("3. Listar Entregas")
            print("4. Listar Alocações das Entregas")
            print("5. Despachar entrega")
            print("6. Finalizar entrega")
            print("7. Cancelar Entrega")
            print("8. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_entrega()
            elif opcao == "2":
                self.alocar_entregas()
            elif opcao == "3":
                self.listar_entregas()
            elif opcao == "4":
                self.exibir_alocacoes()
            elif opcao == "5":
                self.colocar_entrega_em_rota()
            elif opcao == "6":
                self.finalizar_entrega()
            elif opcao == "7":
                self.cancelar_entrega()
            elif opcao == "8":
                print("Retornando ao menu principal...")
                break
            else:
                print("Opção inválida! Tente novamente.")


    def alocar_entregas(self):
        self.logistica.alocar_caminhoes()

    def cadastrar_entrega(self):
        print("\n--- Cadastrar Entrega ---")
        peso = float(input("Digite o peso da entrega (em kg): "))
        volume = float(input("Digite o volume da entrega: "))
        prazo = datetime.now() + timedelta(days=int(input("Digite o prazo de entrega (em dias): ")))
        clientes = self.banco_de_dados.listar_clientes()
        print("\n --- Clientes disponíveis ---\n")
        for cliente_cadastrado in clientes:
            print(f"{cliente_cadastrado.id}: {cliente_cadastrado.nome} | "
                  f"Endereço: {cliente_cadastrado.endereco} - {cliente_cadastrado.cidade}, {cliente_cadastrado.estado}")

        cliente_id = int(input("Digite o ID do cliente: "))
        cliente = self.banco_de_dados.buscar_cliente_por_id(cliente_id)
        if not cliente:
            print(f"Cliente com o id '{cliente_id} não encontrado no banco de dados.")
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

        self.session.add(entrega)
        self.session.commit()
        self.logistica.alocar_caminhoes()
        print("Entrega cadastrada com sucesso!")

    def listar_entregas(self):
        print("\n--- Lista de Entregas ---")
        entregas = self.session.query(Entrega).all()
        if not entregas:
            print("Nenhuma entrega cadastrada.")
        else:
            for entrega in entregas:
                status = f"{entrega.status}".replace("StatusEntrega.", "").replace("_", " ").title()
                prazo = self.__formatar_data(f"{entrega.prazo}")
                print(
                    f"Código: {entrega.id} | Peso: {entrega.peso} kg | Prazo: {prazo} | Status: {status}"
                )

    def colocar_entrega_em_rota(self):
        self.listar_entregas()
        id_entrega = int(input("Selecione a entrega que deseja despachar: "))
        entrega = self.session.query(Entrega).get(id_entrega)
        if not entrega:
            print("Entrega não encontrada.")
            return
        if entrega.status == StatusEntrega.ENTREGUE:
            print("Entrega já foi finalizada.")
            return

        entrega.status = StatusEntrega.EM_ROTA
        self.session.commit()
        print("Status da entrega atualizado com sucesso!")

    def cancelar_entrega(self):
        self.listar_entregas()
        id_entrega = int(input("Selecione a entrega que deseja cancelar: "))
        entrega = self.banco_de_dados.buscar_entrega_por_id(id_entrega)
        if not entrega:
            print("Entrega não encontrada.")
            return

        if entrega.status == StatusEntrega.ENTREGUE:
            print("Entrega já foi finalizada.")
            return

        entrega.status = StatusEntrega.CANCELADA
        self.session.commit()
        print("Entrega cancelada com sucesso!")

    def exibir_alocacoes(self):
        rotas = self.banco_de_dados.listar_rotas()
        if rotas.__len__() == 0:
            print("Não há entregas alocadas para exibir")
            return
        print("\n --- Entregas alocadas ---")

        for rota in rotas:
            caminhao = self.banco_de_dados.buscar_caminhao_por_id(rota.entrega_id)
            centro_distribuicao = self.banco_de_dados.buscar_centro_por_id(caminhao.centro_distribuicao_id)
            entrega = self.banco_de_dados.buscar_entrega_por_id(rota.entrega_id)
            status = f"{entrega.status}".replace("StatusEntrega.", "").replace("_", " ").title()
            prazo = entrega.prazo.strftime("%d/%m/%Y %H:%M")
            print(f"ID: {rota.entrega_id}"
                  f" | Centro responsável: {centro_distribuicao.nome}"
                  f" | Caminhão alocado: {caminhao.modelo} - {caminhao.placa}"
                  f" | Distância total: {rota.distancia_total:.2f} | Custo total: R$ {rota.custo_total:.2f}"
                  f" | Prazo: {prazo} | Status: {status}")


    def finalizar_entrega(self):
        self.listar_entregas()
        id = int(input("Selecione a entrega que deseja finalizar: "))
        entrega = self.banco_de_dados.buscar_entrega_por_id(id)
        if not entrega:
            print("Entrega não encontrada.")
            return

        entrega.status = StatusEntrega.ENTREGUE
        rota = self.banco_de_dados.buscar_rota_por_id(entrega.rota_id)

        rota.data_fim = datetime.now()
        self.session.commit()
        print("Entrega finalizada com sucesso!")


    @staticmethod
    def __formatar_data(string_data: str) -> str:
        date_object = datetime.strptime(string_data, "%Y-%m-%d %H:%M:%S.%f")
        return date_object.strftime("%d/%m/%Y %H:%M")

