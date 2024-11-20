from database.config import get_session
from repository.banco_dados import BancoDados, ErroBancoDados


class MenuCentrosDistribuicao:
    def __init__(self):
        self.session = get_session()
        self.banco_de_dados = BancoDados(session=self.session)

    def menu_centros_distribuicao(self):
        pass