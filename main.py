from database.config import get_session
from database.init_db import init_database, inserir_dados_iniciais
from repository.banco_dados import BancoDados
from visual.menu_principal import MenuPrincipal


def main():
    init_database()
    session = get_session()

    inserir_dados_iniciais(session)

    MenuPrincipal().exibir_menu_principal()

    session.close()


if __name__ == '__main__':
    main()