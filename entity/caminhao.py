class Caminhao:
    def __init__(self, id, capacidade, horas_operacao, centro_distribuicao):
        self.id = id
        self.capacidade = capacidade
        self.horas_operacao = horas_operacao
        self.centro_distribuicao = centro_distribuicao
        self.carga_atual = 0
        self.horas_trabalhadas = 0

    def pode_transportar(self, peso):
        return self.carga_atual + peso <= self.capacidade

    def adicionar_carga(self, peso):
        if self.pode_transportar(peso):
            self.carga_atual += peso
        else:
            raise ValueError("Excedeu a capacidade de carga do caminhão.")

    def pode_trabalhar(self, horas):
        return self.horas_trabalhadas + horas <= self.horas_operacao

    def adicionar_horas(self, horas):
        if self.pode_trabalhar(horas):
            self.horas_trabalhadas += horas
        else:
            raise ValueError("Excedeu o limite de horas de operação do caminhão.")

    def __str__(self):
        return f"Caminhão {self.id} - Capacidade: {self.capacidade}kg, Horas Operação: {self.horas_operacao}, Centro: {self.centro_distribuicao}"
