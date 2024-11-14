from database.config import get_session
from database.init_db import init_database
from models.caminhao import Caminhao
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega
from repository.banco_dados import BancoDados
from service.sistema_logistico import Logistica
from util.calcular_distancia import CalcularDistancia
from visual.menu_caminhoes import MenuCaminhoes
from visual.menu_entrega import MenuEntrega


def main():
    init_database()
    session = get_session()

    banco_de_dados = BancoDados(session=session)


    centro_sp: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-SP")
    centro_pr: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PR")
    centro_pe: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PE")
    centro_pa: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PA")

    centros_distribuicao = banco_de_dados.listar_centros()

    menu_caminhoes = MenuCaminhoes()
    menu_caminhoes.exibir_menu()
    caminhoes = banco_de_dados.listar_caminhoes()

    menu_entregas = MenuEntrega()
    menu_entregas.menu_entrega()
    entregas = banco_de_dados.listar_entregas()

    calculadora_distancia = CalcularDistancia()

    logistica = Logistica(centros=centros_distribuicao, caminhoes=caminhoes, entregas=entregas,
                          calculadora_distancia=calculadora_distancia)

    alocacao = logistica.alocar_caminhoes()

    logistica.exibir_alocacao(alocacao)

    session.close()


if __name__ == '__main__':
    init_database()
    main()