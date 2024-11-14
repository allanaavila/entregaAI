from datetime import datetime

from database.config import get_session
from models.caminhao import Caminhao
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega
from models.rota import Rota
from service.sistema_logistico import Logistica
from util.calcular_distancia import CalcularDistancia


def main():
    session = get_session()

    centros_distribuicao = session.query(CentroDistribuicao).all()

    caminhoes = [
        Caminhao(id=1, placa="ABC-1234", modelo="Truck A", capacidade=10000, velocidade_media=80, custo_km=3.0),
        Caminhao(id=2, placa="XYZ-5678", modelo="Truck B", capacidade=8000, velocidade_media=70, custo_km=3.5)
    ]

    session.add_all(caminhoes)
    session.commit()



    entregas = [
        Entrega(id=1, codigo="E001", peso=5000, volume=10, prazo=datetime(2024, 11, 15, 10, 0),
                endereco_entrega="Rua C, São Paulo, SP", cidade_entrega="São Paulo", estado_entrega="SP", cliente_id=1),
        Entrega(id=2, codigo="E002", peso=3000, volume=5, prazo=datetime(2024, 11, 16, 10, 0),
                endereco_entrega="Rua D, Rio de Janeiro, RJ", cidade_entrega="Rio de Janeiro", estado_entrega="RJ",
                cliente_id=2)
    ]

    session.add_all(entregas)
    session.commit()


    calculadora_distancia = CalcularDistancia()

    centros = {centro.nome: centro.endereco for centro in centros_distribuicao}
    destinos = {entrega.codigo: entrega.endereco_entrega for entrega in entregas}

    calculadora_distancia.construir_grafo(centros_distribuicao, destinos)

    logistica = Logistica(centros=centros_distribuicao, caminhoes=caminhoes, entregas=entregas,
                          calculadora_distancia=calculadora_distancia)

    alocacao = logistica.alocar_caminhoes()

    logistica.exibir_alocacao(alocacao)

    session.close()

if __name__ == "__main__":
    main()
