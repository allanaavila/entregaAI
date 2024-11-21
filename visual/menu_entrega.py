from datetime import datetime, timedelta

from database.config import get_session
from models.entrega import Entrega
from repository.banco_dados import BancoDados
from service.sistema_logistico import Logistica


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
            print("5. Atualizar Status de Entrega")
            print("6. Cancelar Entrega")
            print("7. Voltar ao menu principal")
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
                self.atualizar_entrega()
            elif opcao == "6":
                self.remover_entrega()
            elif opcao == "7":
                print("Retornando ao menu principal...")
                break
            else:
                print("Opção inválida! Tente novamente.")


    def alocar_entregas(self):
        self.logistica.alocar_caminhoes()

    def cadastrar_entrega(self):
        print("\n--- Cadastrar Entrega ---")
        codigo = input("Digite o código da entrega: ")
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
            codigo=codigo,
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
                status = f"{entrega.status}".replace("StatusEntrega.", "").title()
                prazo = self.__formatar_data(f"{entrega.prazo}")
                print(
                    f"Código: {entrega.codigo} | Peso: {entrega.peso} kg | Prazo: {prazo} | Status: {status}"
                )

    def atualizar_entrega(self):
        self.listar_entregas()
        id_entrega = int(input("Digite o ID da entrega que deseja atualizar: "))
        entrega = self.session.query(Entrega).get(id_entrega)
        if not entrega:
            print("Entrega não encontrada.")
            return

        novo_status = input(f"Novo status ({entrega.status}): ")
        entrega.status = novo_status or entrega.status
        self.session.commit()
        print("Status da entrega atualizado com sucesso!")

    def remover_entrega(self):
        self.listar_entregas()
        id_entrega = int(input("Digite o ID da entrega que deseja remover: "))
        entrega = self.session.query(Entrega).get(id_entrega)
        if not entrega:
            print("Entrega não encontrada.")
            return

        self.session.delete(entrega)
        self.session.commit()
        print("Entrega removida com sucesso!")

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
            prazo = entrega.prazo.strftime("%d/%m/%Y %H:%M")
            print(f"ID: {rota.entrega_id}"
                  f" | Centro responsável: {centro_distribuicao.nome}"
                  f" | Caminhão alocado: {caminhao.modelo} - {caminhao.placa}"
                  f" | Distância total: {rota.distancia_total:.2f} | Custo total: R$ {rota.custo_total:.2f}"
                  f" | Prazo: {prazo}")


    @staticmethod
    def __formatar_data(string_data: str) -> str:
        date_object = datetime.strptime(string_data, "%Y-%m-%d %H:%M:%S.%f")
        return date_object.strftime("%d/%m/%Y %H:%M")

