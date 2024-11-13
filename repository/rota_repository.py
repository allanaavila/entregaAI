import logging


class RotaRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def salvar(self, rota):
        try:
            if not rota['origem'] or not rota['destino']:
                raise ValueError("Origem e Destino não podem ser vazios.")

            self.banco_dados.salvar_rota(rota)
            self.logger.info(f"Rota de {rota['origem']} para {rota['destino']} salva com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar a rota de {rota['origem']} para {rota['destino']}: {e}")
            print(f"Erro ao salvar a rota de {rota['origem']} para {rota['destino']}: {e}")

    def buscar(self, origem, destino):
        try:
            rota = self.banco_dados.buscar_rota(origem, destino)
            if rota:
                return rota
            else:
                self.logger.warning(f"Rota de {origem} para {destino} não encontrada.")
                print(f"Rota de {origem} para {destino} não encontrada.")
                return None
        except Exception as e:
            self.logger.error(f"Erro ao buscar a rota de {origem} para {destino}: {e}")
            print(f"Erro ao buscar a rota de {origem} para {destino}: {e}")
            return None

    def listar_todas(self):
        try:
            rotas = self.banco_dados.listar_rotas()
            return rotas
        except Exception as e:
            self.logger.error(f"Erro ao listar rotas: {e}")
            print(f"Erro ao listar rotas: {e}")
            return []

    def atualizar(self, origem, destino, novos_dados):
        try:
            if not novos_dados:
                raise ValueError("Novos dados não podem ser vazios.")

            self.banco_dados.atualizar_rota(origem, destino, novos_dados)
            self.logger.info(f"Rota de {origem} para {destino} atualizada com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao atualizar a rota de {origem} para {destino}: {e}")
            print(f"Erro ao atualizar a rota de {origem} para {destino}: {e}")

    def remover(self, origem, destino):
        try:
            rota = self.banco_dados.buscar_rota(origem, destino)
            if not rota:
                raise ValueError(f"Rota de {origem} para {destino} não encontrada.")

            self.banco_dados.remover_rota(origem, destino)
            self.logger.info(f"Rota de {origem} para {destino} removida com sucesso.")
        except Exception as e:
            self.logger.error(f"Erro ao remover a rota de {origem} para {destino}: {e}")
            print(f"Erro ao remover a rota de {origem} para {destino}: {e}")
