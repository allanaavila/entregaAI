import logging

class CentroDistribuicaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def salvar(self, centro):
        try:
            if not centro.nome:
                raise ValueError("Nome do centro de distribuição não pode ser vazio.")

            self.banco_dados.salvar_centro(centro)
            self.logger.info(f"Centro de Distribuição {centro.nome} salvo com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar o centro de distribuição {centro.nome}: {e}")
            print(f"Erro ao salvar o centro de distribuição {centro.nome}: {e}")

    def buscar(self, nome):
        try:
            centro = self.banco_dados.buscar_centro(nome)
            if centro:
                return centro
            else:
                self.logger.warning(f"Centro de Distribuição {nome} não encontrado.")
                print(f"Centro de Distribuição {nome} não encontrado.")
                return None
        except Exception as e:
            self.logger.error(f"Erro ao buscar o centro de distribuição {nome}: {e}")
            print(f"Erro ao buscar o centro de distribuição {nome}: {e}")
            return None

    def listar_todos(self):
        try:
            centros = self.banco_dados.listar_centros()
            return centros
        except Exception as e:
            self.logger.error(f"Erro ao listar centros de distribuição: {e}")
            print(f"Erro ao listar centros de distribuição: {e}")
            return []

    def atualizar(self, nome, novos_dados):
        try:
            if not novos_dados:
                raise ValueError("Novos dados não podem ser vazios.")

            self.banco_dados.atualizar_centro(nome, novos_dados)
            self.logger.info(f"Centro de Distribuição {nome} atualizado com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao atualizar o centro de distribuição {nome}: {e}")
            print(f"Erro ao atualizar o centro de distribuição {nome}: {e}")

    def remover(self, nome):
        try:
            centro = self.banco_dados.buscar_centro(nome)
            if not centro:
                raise ValueError(f"Centro de distribuição {nome} não encontrado.")

            self.banco_dados.remover_centro(nome)
            self.logger.info(f"Centro de Distribuição {nome} removido com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao remover o centro de distribuição {nome}: {e}")
            print(f"Erro ao remover o centro de distribuição {nome}: {e}")
