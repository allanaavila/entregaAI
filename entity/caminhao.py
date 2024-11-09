class Caminhao:
    def __init__(self, id, capacidade_maxima, horas_operacao):
        self.id = id
        self.capacidade_maxima = capacidade_maxima
        self.horas_operacao = horas_operacao
        self.carga_atual = 0

    def pode_carregar(self, peso):
        return self.carga_atual + peso <= self.capacidade_maxima

    def __str__(self):
        return f"Caminhão {self.id}"
