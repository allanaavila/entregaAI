class CentroDistribuicao:
    _contador_id = 1

    def __init__(self, nome, id=None):
        self.id = id if id else CentroDistribuicao._gerar_id()
        self.nome = nome
        self.caminhoes = []

    @classmethod
    def _gerar_id(cls):
        id_gerado = cls._contador_id
        cls._contador_id += 1
        return id_gerado

    def adicionar_caminhao(self, caminhao):
        self.caminhoes.append(caminhao)

    def __str__(self):
        return f"Centro: {self.nome}, ID: {self.id}"
