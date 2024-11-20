from datetime import datetime

from database.config import get_session
from models.entrega import Entrega
from repository.banco_dados import BancoDados


class MenuEntregas:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def menu_principal(self):
        while True:
            print("\n--- Menu de Entregas ---")
            print("1. Cadastrar Entrega")
            print("2. Listar Entregas")
            print("3. Atualizar Status de Entrega")
            print("4. Remover Entrega")
            print("5. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_entrega()
            elif opcao == "2":
                self.listar_entregas()
            elif opcao == "3":
                self.atualizar_entrega()
            elif opcao == "4":
                self.remover_entrega()
            elif opcao == "5":
                print("Retornando ao menu principal...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def cadastrar_entrega(self):
        print("\n--- Cadastrar Entrega ---")
        codigo = input("Digite o código da entrega: ")
        peso = float(input("Digite o peso da entrega (em kg): "))
        volume = float(input("Digite o volume da entrega: "))
        prazo_str = input("Digite o prazo de entrega (YYYY-MM-DD HH:MM): ")
        prazo = datetime.strptime(prazo_str, "%Y-%m-%d %H:%M")
        endereco = input("Digite o endereço de entrega: ")
        cidade = input("Digite a cidade de entrega: ")
        estado = input("Digite o estado de entrega: ")
        cliente_id = int(input("Digite o ID do cliente: "))
        latitude = float(input("Digite a latitude: "))
        longitude = float(input("Digite a longitude: "))

        entrega = Entrega(
            codigo=codigo,
            peso=peso,
            volume=volume,
            prazo=prazo,
            endereco_entrega=endereco,
            cidade_entrega=cidade,
            estado_entrega=estado,
            latitude_entrega=latitude,
            longitude_entrega=longitude,
            cliente_id=cliente_id
        )

        self.session.add(entrega)
        self.session.commit()
        print("Entrega cadastrada com sucesso!")

    def listar_entregas(self):
        print("\n--- Lista de Entregas ---")
        entregas = self.session.query(Entrega).all()
        if not entregas:
            print("Nenhuma entrega cadastrada.")
        else:
            for entrega in entregas:
                print(
                    f"Código: {entrega.codigo} | Peso: {entrega.peso} kg | Prazo: {entrega.prazo} | Status: {entrega.status}"
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
