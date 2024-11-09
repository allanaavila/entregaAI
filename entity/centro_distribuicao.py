class CentroDistribuicao:
    def __init__(self, nome, id=None):
        self.id = id
        self.nome = nome
        self.caminhoes = []

    def adicionar_caminhao(self, caminhao):
        self.caminhoes.append(caminhao)

    def __str__(self):
        return f"Centro: {self.nome}, ID: {self.id}"
