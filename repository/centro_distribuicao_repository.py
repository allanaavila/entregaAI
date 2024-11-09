class CentroDistribuicaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, centro):
        self.banco_dados.salvar_centro(centro)

    def buscar(self, nome):
        return self.banco_dados.buscar_centro(nome)

    def listar_todos(self):
        return self.banco_dados.listar_centros()
