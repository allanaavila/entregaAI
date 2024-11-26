from datetime import datetime

from database.config import get_session
from models import entrega, cliente, caminhao
from models.caminhao import Caminhao
from models.centro_distribuicao import CentroDistribuicao
from models.cliente import Cliente
from models.entrega import Entrega
from util.encontrar_localizacao import obter_coordenadas_opencage
from util.validar_cnpj import validar_cnpj


class Cadastro:
    def  __init__(self: Caminhao, Entrega, Cliente):
        self.caminhao = caminhao
        self.entrega = entrega
        self.cliente = cliente


    def adicionar_caminhao(self):
        session = get_session()
        centros = session.query(CentroDistribuicao).all()
        if not centros:
            print("Nenhum centro de distribuição disponível.")
            return

        print("\n--- Adicionar Caminhão ---")
        print("Escolha um centro de distribuição:")
        for i, centro in enumerate(centros, start=1):
            print(f"{i}. {centro.nome} ({centro.cidade}, {centro.estado})")

        centro_index = int(input("Digite o número do centro: ")) - 1
        if centro_index < 0 or centro_index >= len(centros):
            print("Opção inválida.")
            return

        centro_selecionado = centros[centro_index]

        placa = input("Digite a placa do caminhão: ")
        modelo = input("Digite o modelo do caminhão: ")
        capacidade = float(input("Digite a capacidade do caminhão (em kg): "))

        caminhao = Caminhao(
            placa=placa,
            modelo=modelo,
            capacidade=capacidade,
            centro_distribuicao_id=centro_selecionado.id
        )

        session.add(caminhao)
        session.commit()
        print(f"Caminhão cadastrado no centro {centro_selecionado.nome}.")
        session.close()

    def adicionar_cliente(self):
        session = get_session()

        print("\n    📋  Adicionar Cliente  📋   ")
        nome = input("Digite o nome do cliente: ")
        cnpj = input("Digite o CNPJ do cliente: ")

        cnpj_validado = validar_cnpj(cnpj)
        if not cnpj_validado:
            print("\n❌ CNPJ inválido. Verifique e tente novamente.")
            return

        endereco = input("Digite o endereço do cliente: ")
        cidade = input("Digite a cidade do cliente: ")
        estado = input("Digite o estado do cliente: ")

        print("\n🔍 Obtendo a localização do cliente...")
        coordenadas = obter_coordenadas_opencage(endereco, cidade, estado)

        if type(coordenadas) == dict:
            print(f"\n❌ Erro ao obter localização: {coordenadas['erro']}")
            return
        else:
            latitude, longitude = coordenadas

        print("\n🔒 Confirme os dados antes de salvar:")
        print(f"\nNome      : {nome}")
        print(f"CNPJ      : {cnpj_validado}")
        print(f"Endereço  : {endereco}")
        print(f"Cidade    : {cidade}")
        print(f"Estado    : {estado}")
        print(f"Latitude  : {latitude}")
        print(f"Longitude : {longitude}")

        confirmacao = input("\n✅ Confirmar cadastro? (S/N): ").strip().lower()

        if confirmacao != 's':
            print("\n❌ Cadastro cancelado.")
            return

        cliente = Cliente(
            nome=nome,
            cnpj=cnpj_validado,
            endereco=endereco,
            cidade=cidade,
            estado=estado,
            latitude=latitude,
            longitude=longitude
        )

        try:
            session.add(cliente)
            session.commit()
            print("\n✅ Cliente cadastrado com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar cliente: {e}")
            session.rollback()
        finally:
            session.close()


    def adicionar_entrega(self):
        session = get_session()
        clientes = session.query(Cliente).all()
        if not clientes:
            print("Nenhum cliente cadastrado.")
            return

        print("\n--- Adicionar Entrega ---")
        print("Escolha um cliente:")
        for i, cliente in enumerate(clientes, start=1):
            print(f"{i}. {cliente.nome} - CNPJ: {cliente.cnpj}")

        cliente_index = int(input("Digite o número do cliente: ")) - 1
        if cliente_index < 0 or cliente_index >= len(clientes):
            print("Opção inválida.")
            return

        cliente_selecionado = clientes[cliente_index]

        codigo = input("Digite o código da entrega: ")
        peso = float(input("Digite o peso da entrega (em kg): "))
        volume = float(input("Digite o volume da entrega: "))
        prazo_str = input("Digite o prazo da entrega (formato: YYYY-MM-DD HH:MM): ")
        prazo = datetime.strptime(prazo_str, "%Y-%m-%d %H:%M")
        prioridade = input("Digite a prioridade da entrega (Alta, Média, Baixa): ")
        status = input("Digite o status da entrega (Pendente, Em trânsito, Concluída): ")

        entrega = Entrega(
            codigo=codigo,
            peso=peso,
            volume=volume,
            prazo=prazo,
            prioridade=prioridade,
            status=status,
            cliente_id=cliente_selecionado.id,
            endereco_entrega=cliente_selecionado.endereco,
            cidade_entrega=cliente_selecionado.cidade,
            estado_entrega=cliente_selecionado.estado,
            latitude_entrega=cliente_selecionado.latitude,
            longitude_entrega=cliente_selecionado.longitude
        )

        session.add(entrega)
        session.commit()
        print("Entrega cadastrada com sucesso!")
        session.close()

