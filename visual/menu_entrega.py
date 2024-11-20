from datetime import datetime

from database.config import get_session
from models.entrega import Entrega
from repository.banco_dados import BancoDados, ErroBancoDados


class MenuEntrega:

    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def menu_entrega(self):
        while True:
            print("\n--- Menu de Entregas ---")
            print("1. Cadastrar Entrega")
            print("2. Listar todas as Entregas")
            print("3. Cancelar Entrega")
            print("4. Voltar menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_entrega()
            elif opcao == "2":
                self.listar_entregas()
            elif opcao == "4":
                print("Encerrando o programa...")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def cadastrar_entrega(self):
        print("\n--- Cadastrar Entrega ---")
        codigo = input("Digite o código da entrega: ")
        peso = float(input("Digite o peso da entrega (em kg): "))
        volume = float(input("Digite o volume da entrega: "))
        prazo_str = input("Digite o prazo da entrega (formato: YYYY-MM-DD HH:MM): ")
        prazo = datetime.strptime(prazo_str, "%Y-%m-%d %H:%M")
        endereco = input("Digite o endereço de entrega: ")
        cidade = input("Digite a cidade de entrega: ")
        estado = input("Digite o estado de entrega: ")
        cliente_id = int(input("Digite o ID do cliente: "))
        latitude = float(input("Digite a latitude da entrega: "))
        longitude = float(input("Digite a longitude da entrega: "))

        entrega = Entrega(
            codigo=codigo,
            peso=peso,
            volume=volume,
            prazo=prazo,
            endereco_entrega=endereco,
            cidade_entrega=cidade,
            estado_entrega=estado,
            cliente_id=cliente_id,
            latitude_entrega=latitude,
            longitude_entrega=longitude
        )

        self.session.add(entrega)
        self.session.commit()
        print("Entrega cadastrada com sucesso!")
        self.session.close()

    def listar_entregas(self):
        session = get_session()
        banco_de_dados = BancoDados(session=session)

        print("\n--- Listar Entregas ---")
        entregas = banco_de_dados.listar_entregas()

        if not entregas:
            print("Nenhuma entrega cadastrada.")
        else:
            for entrega in entregas:
                print(
                    f"\n--- Detalhes da Entrega ---\n"
                    f"ID da Entrega: {entrega.id}\n"
                    f"Código da Entrega: {entrega.codigo}\n"
                    f"Peso: {entrega.peso:.2f} kg\n"
                    f"Volume: {entrega.volume:.2f} m³\n"
                    f"Prazo de Entrega: {entrega.prazo.strftime('%d/%m/%Y %H:%M')}\n"
                    f"Endereço: {entrega.endereco_entrega}\n"
                    f"Cidade: {entrega.cidade_entrega}\n"
                    f"Estado: {entrega.estado_entrega}\n"
                    f"Localização: Latitude {entrega.latitude_entrega}, Longitude {entrega.longitude_entrega}\n"
                )

        session.close()