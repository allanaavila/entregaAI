import logging


class CaminhaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def salvar(self, caminhao, centro_nome):
        try:
            if not self.banco_dados.existe_centro(centro_nome):
                raise ValueError(f"Centro de distribuição '{centro_nome}' não existe.")
            self.banco_dados.salvar_caminhao(caminhao, centro_nome)
            self.logger.info(f"Caminhão {caminhao.id} salvo no centro {centro_nome}.")
        except Exception as e:
            self.logger.error(f"Erro ao salvar o caminhão {caminhao.id}: {e}")
            print(f"Erro ao salvar o caminhão {caminhao.id}: {e}")

    def listar_todos(self):
        try:
            caminhoes = self.banco_dados.listar_caminhoes()
            return caminhoes
        except Exception as e:
            self.logger.error(f"Erro ao listar caminhões: {e}")
            print(f"Erro ao listar caminhões: {e}")
            return []

    def listar_por_centro(self, centro_nome):
        try:
            caminhoes = self.banco_dados.listar_caminhoes_por_centro(centro_nome)
            return caminhoes
        except Exception as e:
            self.logger.error(f"Erro ao listar caminhões do centro {centro_nome}: {e}")
            print(f"Erro ao listar caminhões do centro {centro_nome}: {e}")
            return []

    def atualizar_carga(self, caminhao_id, nova_carga):
        try:
            if not self.banco_dados.existe_caminhao(caminhao_id):
                raise ValueError(f"Caminhão com ID {caminhao_id} não encontrado.")
            self.banco_dados.atualizar_carga_caminhao(caminhao_id, nova_carga)
            self.logger.info(f"Carga do caminhão {caminhao_id} atualizada para {nova_carga} kg.")
        except Exception as e:
            self.logger.error(f"Erro ao atualizar carga do caminhão {caminhao_id}: {e}")
            print(f"Erro ao atualizar carga do caminhão {caminhao_id}: {e}")

    def remover(self, caminhao_id):
        try:
            if not self.banco_dados.existe_caminhao(caminhao_id):
                raise ValueError(f"Caminhão com ID {caminhao_id} não encontrado.")
            self.banco_dados.remover_caminhao(caminhao_id)
            self.logger.info(f"Caminhão {caminhao_id} removido do banco de dados.")
        except Exception as e:
            self.logger.error(f"Erro ao remover o caminhão {caminhao_id}: {e}")
            print(f"Erro ao remover o caminhão {caminhao_id}: {e}")