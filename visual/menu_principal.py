from database.config import get_session
from repository.banco_dados import BancoDados
from visual.menu_caminhoes import MenuCaminhoes
from visual.menu_cliente import MenuCliente
from visual.menu_entrega import MenuEntrega


class MenuPrincipal:

    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)


    def exibir_menu_principal(self):
        while True:
            print("\n--- Menu de Principal ---")
            print("1. Menu entregas")
            print("2. Menu caminhoes")
            print("3. Menu clientes")
            print("4. Sair")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                MenuEntrega.menu_entrega()
            elif opcao == "2":
                MenuCaminhoes.exibir_menu()
            elif opcao == "3":
                MenuCliente.exibir_menu_cliente()
            elif opcao == "4":
                break
            else:
                print("Opção inválida! Tente novamente.")