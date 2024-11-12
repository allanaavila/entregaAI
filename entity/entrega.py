class Entrega:
    def __init__(self, destino, prazo_entrega, peso, prioridade):
        if peso <= 0:
            raise ValueError("O peso da entrega deve ser maior que zero.")
        self.destino = destino
        self.prazo_entrega = prazo_entrega
        self.peso = peso
        self.prioridade = prioridade
        self.status = "Pendente"

    def __str__(self):
        return f"(Destino: {self.destino}, Prazo: {self.prazo_entrega}, Peso: {self.peso} kg, Prioridade: {self.prioridade}, Status: {self.status})"
