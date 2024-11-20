from database.config import get_session
from models.centro_distribuicao import CentroDistribuicao
from repository.banco_dados import BancoDados
from util.encontrar_localizacao import obter_coordenadas_opencage


class MenuCentrosDistribuicao:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def menu_principal(self):
        while True:
            print("\n--- Menu Centros de Distribuição ---")
            print("1. Adicionar Centro de Distribuição")
            print("2. Listar Centros de Distribuição")
            print("3. Atualizar Centro de Distribuição")
            print("4. Remover Centro de Distribuição")
            print("5. Voltar ao menu principal")
            opcao = input("Escolha uma opção: ")

            if opcao == "1":
                self.adicionar_centro()
            elif opcao == "2":
                self.listar_centros()
            elif opcao == "3":
                self.atualizar_centro()
            elif opcao == "4":
                self.remover_centro()
            elif opcao == "5":
                print("Saindo do sistema... Até logo!")
                break
            else:
                print("Opção inválida! Tente novamente.")

    def adicionar_centro(self):
        print("\n--- Adicionar Centro de Distribuição ---")
        nome = input("Digite o nome do centro: ")
        endereco = input("Digite o endereço: ")
        cidade = input("Digite a cidade: ")
        estado = input("Digite o estado (UF): ")
        capacidade_maxima = float(input("Digite a capacidade máxima (em kg): "))

        coordenadas = obter_coordenadas_opencage(endereco, cidade, estado)
        if isinstance(coordenadas, dict):
            print(f"Erro ao obter localização: {coordenadas['erro']}")
            return
        latitude, longitude = coordenadas

        centro = CentroDistribuicao(
            nome=nome,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            capacidade_maxima=capacidade_maxima,
            latitude=latitude,
            longitude=longitude
        )

        self.session.add(centro)
        self.session.commit()
        print("Centro de Distribuição cadastrado com sucesso!")

    def listar_centros(self):
        print("\n--- Lista de Centros de Distribuição ---")
        centros = self.session.query(CentroDistribuicao).all()
        if not centros:
            print("Nenhum centro de distribuição cadastrado.")
        else:
            for centro in centros:
                print(
                    f"ID: {centro.id} | Nome: {centro.nome} | Cidade: {centro.cidade} | Estado: {centro.estado} | Capacidade: {centro.capacidade_maxima} kg"
                )

    def atualizar_centro(self):
        self.listar_centros()
        id_centro = int(input("Digite o ID do centro que deseja atualizar: "))
        centro = self.session.query(CentroDistribuicao).get(id_centro)
        if not centro:
            print("Centro de Distribuição não encontrado.")
            return

        print("\n--- Atualizar Centro de Distribuição ---")
        centro.nome = input(f"Novo nome ({centro.nome}): ") or centro.nome
        centro.capacidade_maxima = float(
            input(f"Nova capacidade máxima ({centro.capacidade_maxima} kg): ")
        ) or centro.capacidade_maxima

        self.session.commit()
        print("Centro atualizado com sucesso!")

    def remover_centro(self):
        self.listar_centros()
        id_centro = int(input("Digite o ID do centro que deseja remover: "))
        centro = self.session.query(CentroDistribuicao).get(id_centro)
        if not centro:
            print("Centro de Distribuição não encontrado.")
            return

        self.session.delete(centro)
        self.session.commit()
        print("Centro removido com sucesso!")
