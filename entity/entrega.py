class Entrega:
    def __init__(self, destino, prazo_entrega, peso):
        self.destino = destino
        self.prazo_entrega = prazo_entrega
        self.peso = peso

    def __str__(self):
        return f"(Destino: {self.destino}, Prazo: {self.prazo_entrega}, Peso: {self.peso} kg)"
