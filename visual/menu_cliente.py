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
            print("\n--- Menu de Clientes ---")
            print("1. Cadastrar Cliente")
            print("2. Listar Clientes")
            print("3. Remover Cliente")
            print("4. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.cadastrar_cliente()
            elif opcao == "2":
                self.listar_cliente()
            elif opcao == "3":
                self.remover_cliente()
            elif opcao == "4":
                break
            else:
                print("Opção Inválida! Tente novamente.")


    def cadastrar_cliente(self):
        cadastro = Cadastro(Entrega, Cliente)
        cadastro.adicionar_cliente()

    def listar_cliente(self):
        print("\n--- Listar Clientes ---")
        clientes = self.banco_de_dados.listar_clientes()

        if not clientes:
            print("Nenhum cliente cadastrado.")
        else:
            for cliente in clientes:
                print(f"ID: {cliente.id}, Nome: {cliente.nome}, CNPJ: {cliente.cnpj}, "
                      f"Endereço: {cliente.endereco}, Cidade: {cliente.cidade}, Estado: {cliente.estado}")


    def remover_cliente(self):
        print("\n--- Remover Cliente ---")
        clientes = self.banco_de_dados.listar_clientes()

        if not clientes:
            print("Nenhum cliente cadastrado.")
            return

        for i, cliente in enumerate(clientes, start=1):
            print(f"{i}. {cliente.nome} - CNPJ: {cliente.cnpj}")

        cliente_index = int(input("Digite o número do cliente a ser removido: ")) - 1
        if cliente_index < 0 or cliente_index >= len(clientes):
            print("Opção inválida.")
            return

        cliente_remover = clientes[cliente_index]

        try:
            self.banco_de_dados.remover_cliente(cliente_remover.id)
            print(f"Cliente {cliente_remover.nome} removido com sucesso!")
        except ErroBancoDados as e:
            print(f"Erro ao remover cliente: {str(e)}")



    def __del__(self):
        self.session.close()


