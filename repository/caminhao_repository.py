class CaminhaoRepository:
    def __init__(self, banco_dados):
        self.banco_dados = banco_dados

    def salvar(self, caminhao, centro_nome):
        self.banco_dados.salvar_caminhao(caminhao, centro_nome)

    def listar_todos(self):
        return self.banco_dados.listar_caminhoes()
