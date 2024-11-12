class CaminhaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, caminhao, centro_nome):
        try:
            self.banco_dados.salvar_caminhao(caminhao, centro_nome)
            print(f"Caminhão {caminhao.id} salvo no centro {centro_nome}.")
        except Exception as e:
            print(f"Erro ao salvar o caminhão {caminhao.id}: {e}")

    def listar_todos(self):
        try:
            return self.banco_dados.listar_caminhoes()
        except Exception as e:
            print(f"Erro ao listar caminhões: {e}")
            return []

    def listar_por_centro(self, centro_nome):
        try:
            return self.banco_dados.listar_caminhoes_por_centro(centro_nome)
        except Exception as e:
            print(f"Erro ao listar caminhões do centro {centro_nome}: {e}")
            return []

    def atualizar_carga(self, caminhao_id, nova_carga):
        try:
            self.banco_dados.atualizar_carga_caminhao(caminhao_id, nova_carga)
            print(f"Carga do caminhão {caminhao_id} atualizada para {nova_carga} kg.")
        except Exception as e:
            print(f"Erro ao atualizar carga do caminhão {caminhao_id}: {e}")

    def remover(self, caminhao_id):
        try:
            self.banco_dados.remover_caminhao(caminhao_id)
            print(f"Caminhão {caminhao_id} removido do banco de dados.")
        except Exception as e:
            print(f"Erro ao remover o caminhão {caminhao_id}: {e}")