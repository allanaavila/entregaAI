class EntregaRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, entrega):
        try:
            self.banco_dados.salvar_entrega(entrega)
            print(f"Entrega para {entrega.destino} salva com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar a entrega para {entrega.destino}: {e}")

    def buscar(self, destino):
        try:
            entrega = self.banco_dados.buscar_entrega(destino)
            if entrega:
                return entrega
            else:
                print(f"Entrega para {destino} não encontrada.")
                return None
        except Exception as e:
            print(f"Erro ao buscar a entrega para {destino}: {e}")
            return None

    def listar_todas(self):
        try:
            return self.banco_dados.listar_entregas()
        except Exception as e:
            print(f"Erro ao listar entregas: {e}")
            return []

    def atualizar(self, destino, novos_dados):
        try:
            self.banco_dados.atualizar_entrega(destino, novos_dados)
            print(f"Entrega para {destino} atualizada com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a entrega para {destino}: {e}")

    def remover(self, destino):
        try:
            self.banco_dados.remover_entrega(destino)
            print(f"Entrega para {destino} removida com sucesso.")
        except Exception as e:
            print(f"Erro ao remover a entrega para {destino}: {e}")
