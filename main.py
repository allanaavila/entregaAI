from database.config import get_session
from database.init_db import init_database
from models.centro_distribuicao import CentroDistribuicao
from repository.banco_dados import BancoDados
from visual.menu_principal import MenuPrincipal


def main():
    init_database()
    session = get_session()

    banco_de_dados = BancoDados(session=session)

    centro_sp: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-SP")
    centro_pr: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PR")
    centro_pe: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PE")
    centro_pa: CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PA")

    centros_distribuicao = banco_de_dados.listar_centros()


    menu_principal = MenuPrincipal()
    menu_principal.exibir_menu_principal()

    session.close()


if __name__ == '__main__':
    init_database()
    main()