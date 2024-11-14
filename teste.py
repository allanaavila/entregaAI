from database.config import get_session
from database.init_db import init_database
from models.centro_distribuicao import CentroDistribuicao
from models.entrega import Entrega
from repository.banco_dados import BancoDados
from service.sistema_logistico import Logistica
from util.calcular_distancia import CalcularDistancia

def main():
    session = get_session()

    banco_de_dados = BancoDados(session=session)

    """
    centros_distribuicao = [
        CentroDistribuicao(
            codigo="CD-PA",
            nome="CD Belém",
            endereco="Endereço CD Belém",
            cidade="Belém",
            estado="PA",
            latitude=-1.4557,
            longitude=-48.4902,
            capacidade_maxima=100000
        ),
        CentroDistribuicao(
            codigo="CD-PE",
            nome="CD Recife",
            endereco="Endereço CD Recife",
            cidade="Recife",
            estado="PE",
            latitude=-8.0476,
            longitude=-34.8770,
            capacidade_maxima=150000
        ),
        CentroDistribuicao(
            codigo="CD-SP",
            nome="CD São Paulo",
            endereco="Endereço CD São Paulo",
            cidade="São Paulo",
            estado="SP",
            latitude=-23.5505,
            longitude=-46.6333,
            capacidade_maxima=200000
        ),
        CentroDistribuicao(
            codigo="CD-PR",
            nome="CD Curitiba",
            endereco="Endereço CD Curitiba",
            cidade="Curitiba",
            estado="PR",
            latitude=-25.4284,
            longitude=-49.2733,
            capacidade_maxima=120000
        )
    ]
    """


    centro_sp:CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-SP", session=session)
    centro_pr:CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PR", session=session)
    centro_pe:CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PE", session=session)
    centro_pa:CentroDistribuicao = banco_de_dados.buscar_centro(codigo="CD-PA", session=session)

    centros_distribuicao = [
        centro_sp,
        centro_pr,
        centro_pa,
        centro_pe
    ]

    caminhoes = banco_de_dados.listar_caminhoes()

    """
    caminhoes = [
        Caminhao(id=1, placa="ABC-1234", modelo="Truck A", capacidade=10000, velocidade_media=80, custo_km=3.0, centro_distribuicao_id=centro_sp.id),
        Caminhao(id=2, placa="XYZ-5678", modelo="Truck B", capacidade=8000, velocidade_media=70, custo_km=3.5, centro_distribuicao_id=centro_pr.id)
    ]
    
    session.add_all(caminhoes)
    session.commit()
    """

    """
    entregas = [
        Entrega(id=1, codigo="E001", peso=5000, volume=10, prazo=datetime(2024, 11, 15, 10, 0),
                endereco_entrega="Rua C, São Paulo, SP", cidade_entrega="São Paulo", estado_entrega="SP", cliente_id=1, latitude_entrega=-23.541250, longitude_entrega=-46.638826),
        Entrega(id=2, codigo="E002", peso=3000, volume=5, prazo=datetime(2024, 11, 16, 10, 0),
                endereco_entrega="Rua Santa Rita, Cidade Jardim", cidade_entrega="São José dos Pinhais", estado_entrega="PR",
                cliente_id=2, latitude_entrega=-25.523217, longitude_entrega=-49.208699),
    ]

    session.add_all(entregas)
    session.commit()
    """

    entregas = session.query(Entrega).all()

    calculadora_distancia = CalcularDistancia()

    logistica = Logistica(centros=centros_distribuicao, caminhoes=caminhoes, entregas=entregas, calculadora_distancia=calculadora_distancia)

    alocacao = logistica.alocar_caminhoes()

    logistica.exibir_alocacao(alocacao)

    session.close()

if __name__ == '__main__':
    init_database()
    main()