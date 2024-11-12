class RotaRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, rota):
        try:
            self.banco_dados.salvar_rota(rota)
            print(f"Rota de {rota['origem']} para {rota['destino']} salva com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar a rota de {rota['origem']} para {rota['destino']}: {e}")

    def buscar(self, origem, destino):
        try:
            rota = self.banco_dados.buscar_rota(origem, destino)
            if rota:
                return rota
            else:
                print(f"Rota de {origem} para {destino} não encontrada.")
                return None
        except Exception as e:
            print(f"Erro ao buscar a rota de {origem} para {destino}: {e}")
            return None

    def listar_todas(self):
        try:
            return self.banco_dados.listar_rotas()
        except Exception as e:
            print(f"Erro ao listar rotas: {e}")
            return []

    def atualizar(self, origem, destino, novos_dados):
        try:
            self.banco_dados.atualizar_rota(origem, destino, novos_dados)
            print(f"Rota de {origem} para {destino} atualizada com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar a rota de {origem} para {destino}: {e}")

    def remover(self, origem, destino):
        try:
            self.banco_dados.remover_rota(origem, destino)
            print(f"Rota de {origem} para {destino} removida com sucesso.")
        except Exception as e:
            print(f"Erro ao remover a rota de {origem} para {destino}: {e}")