import logging


class EntregaRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def salvar(self, entrega):
        try:
            if not entrega.destino:
                raise ValueError("Destino da entrega não pode ser vazio.")

            self.banco_dados.salvar_entrega(entrega)
            self.logger.info(f"Entrega para {entrega.destino} salva com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar a entrega para {entrega.destino}: {e}")
            print(f"Erro ao salvar a entrega para {entrega.destino}: {e}")

    def buscar(self, destino):
        try:
            entrega = self.banco_dados.buscar_entrega(destino)
            if entrega:
                return entrega
            else:
                self.logger.warning(f"Entrega para {destino} não encontrada.")
                print(f"Entrega para {destino} não encontrada.")
                return None
        except Exception as e:
            self.logger.error(f"Erro ao buscar a entrega para {destino}: {e}")
            print(f"Erro ao buscar a entrega para {destino}: {e}")
            return None

    def listar_todas(self):
        try:
            entregas = self.banco_dados.listar_entregas()
            return entregas
        except Exception as e:
            self.logger.error(f"Erro ao listar entregas: {e}")
            print(f"Erro ao listar entregas: {e}")
            return []

    def atualizar(self, destino, novos_dados):
        try:
            if not novos_dados:
                raise ValueError("Novos dados não podem ser vazios.")

            self.banco_dados.atualizar_entrega(destino, novos_dados)
            self.logger.info(f"Entrega para {destino} atualizada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao atualizar a entrega para {destino}: {e}")
            print(f"Erro ao atualizar a entrega para {destino}: {e}")

    def remover(self, destino):
        try:
            entrega = self.banco_dados.buscar_entrega(destino)
            if not entrega:
                raise ValueError(f"Entrega para {destino} não encontrada.")

            self.banco_dados.remover_entrega(destino)
            self.logger.info(f"Entrega para {destino} removida com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao remover a entrega para {destino}: {e}")
            print(f"Erro ao remover a entrega para {destino}: {e}")
