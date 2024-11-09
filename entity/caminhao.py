class Caminhao:
    def __init__(self, id, capacidade_maxima, horas_operacao,carga_atual=0, centro=None):
        self.id = id
        self.capacidade_maxima = capacidade_maxima
        self.horas_operacao = horas_operacao
        self.carga_atual = 0
        self.centro = centro

    def pode_carregar(self, peso):
        return self.carga_atual + peso <= self.capacidade_maxima

    def carregar(self, peso):
        if self.pode_carregar(peso):
            self.carga_atual += peso
            print(f"Carga de {peso} kg carregada no caminhão {self.id}. Carga atual: {self.carga_atual} kg.")
        else:
            print(f"O caminhão {self.id} não tem capacidade para carregar {peso} kg.")

    def __str__(self):
        return f"Caminhão {self.id} (Capacidade: {self.capacidade_maxima} kg, Carga atual: {self.carga_atual} kg, Centro: {self.centro.nome if self.centro else 'N/A'})"

