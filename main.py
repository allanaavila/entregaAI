from models.caminhao import Caminhao
from models.entrega import Entrega
from models.rota import Rota
from service.sistema_logistico import Logistica
from util.calcular_distancia import CalcularDistancia


def main():
    calcular_distancia = CalcularDistancia()
    endereco_inicial = "Avenida Paulista, São Paulo"
    endereco_final = "Rua da Consolação, São Paulo"

    distancia = calcular_distancia.calcular_distancia(endereco_inicial, endereco_final)
    if distancia is not None:
        print(f"A distância ajustada entre os endereços é: {distancia:.2f} km")
    else:
        print("Não foi possível calcular a distância devido a um erro.")



if __name__ == "__main__":
    main()
