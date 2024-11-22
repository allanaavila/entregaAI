from database.config import get_session
from repository.banco_dados import BancoDados
from visual.menu_caminhoes import MenuCaminhoes
from visual.menu_centros import MenuCentrosDistribuicao
from visual.menu_cliente import MenuCliente
from visual.menu_entrega import MenuEntregas


class MenuPrincipal:

    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def exibir_menu_principal(self):
        while True:
            print("\n" + "=" * 60)
            print("                 🌟 Menu Principal 🌟")
            print("=" * 60)
            print("1️⃣  Gerenciar Centros de Distribuição")
            print("2️⃣  Gerenciar Entregas")
            print("3️⃣  Gerenciar Caminhões")
            print("4️⃣  Gerenciar Clientes")
            print("5️⃣  🚪 Sair do Sistema")
            print("=" * 60)
            opcao = input("🔹 Escolha uma opção: ")

            if opcao == "1":
                menu_centros = MenuCentrosDistribuicao()
                menu_centros.menu_principal()
            elif opcao == "2":
                menu_entregas = MenuEntregas()
                menu_entregas.menu_principal()
            elif opcao == "3":
                menu_caminhoes = MenuCaminhoes()
                menu_caminhoes.exibir_menu()
            elif opcao == "4":
                menu_clientes = MenuCliente()
                menu_clientes.exibir_menu_cliente()
            elif opcao == "5":
                print("\n✅ Saindo do sistema... Até logo!")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")

