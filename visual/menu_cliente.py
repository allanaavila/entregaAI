from database.config import get_session
from models.caminhao import Caminhao
from models.cliente import Cliente
from models.entrega import Entrega
from repository.banco_dados import BancoDados, ErroBancoDados
from service.cadastro import Cadastro


class MenuCliente:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def exibir_menu_cliente(self):
        while True:
            print("\n" + "=" * 50)
            print("            👥 Menu de Clientes               ")
            print("=" * 50)
            print("1️⃣  Cadastrar Cliente")
            print("2️⃣  Listar Clientes")
            print("3️⃣  🔙 Voltar ao Menu Principal")
            print("=" * 50)
            opcao = input("🔹 Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.listar_cliente()
            elif opcao == "3":
                print("\n✅ Retornando ao menu principal...")
                break
            else:
                print("\n❌ Opção inválida! Tente novamente.")

    def cadastrar_cliente(self):
        cadastro = Cadastro(Entrega, Cliente)
        cadastro.adicionar_cliente()

    def listar_cliente(self):
        print("\n    📋  Listagem de Clientes  📋   ")
        clientes = self.banco_de_dados.listar_clientes()

        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            print(f"\n{'ID':^10} | {'Nome':^40} | {'CNPJ':^20} | {'Endereço':^40} | {'Cidade':^20} | {'Estado':^10}")
            print("=" * 160)
            for cliente in clientes:
                print(
                    f"{cliente.id:^10} | {cliente.nome:^40} | {cliente.cnpj:^20} | {cliente.endereco:^40} | {cliente.cidade:^20} | {cliente.estado:^10}")
            print("=" * 160)

    def __del__(self):
        self.session.close()


