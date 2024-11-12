class CentroDistribuicaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, centro):
        try:
            self.banco_dados.salvar_centro(centro)
            print(f"Centro de Distribuição {centro.nome} salvo com sucesso.")
        except Exception as e:
            print(f"Erro ao salvar o centro de distribuição {centro.nome}: {e}")

    def buscar(self, nome):
        try:
            centro = self.banco_dados.buscar_centro(nome)
            if centro:
                return centro
            else:
                print(f"Centro de Distribuição {nome} não encontrado.")
                return None
        except Exception as e:
            print(f"Erro ao buscar o centro de distribuição {nome}: {e}")
            return None

    def listar_todos(self):
        try:
            return self.banco_dados.listar_centros()
        except Exception as e:
            print(f"Erro ao listar centros de distribuição: {e}")
            return []

    def atualizar(self, nome, novos_dados):
        try:
            self.banco_dados.atualizar_centro(nome, novos_dados)
            print(f"Centro de Distribuição {nome} atualizado com sucesso.")
        except Exception as e:
            print(f"Erro ao atualizar o centro de distribuição {nome}: {e}")


    def remover(self, nome):
        try:
            self.banco_dados.remover_centro(nome)
            print(f"Centro de Distribuição {nome} removido com sucesso.")
        except Exception as e:
            print(f"Erro ao remover o centro de distribuição {nome}: {e}")
