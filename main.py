from entity.caminhao import Caminhao
from entity.entrega import Entrega
from entity.rota import RotaGrafo
from service.sistema_logistico import Logistica

def main():
    # 1. Criando os centros de distribuição
    centros = ["Belém", "Recife", "São Paulo", "Curitiba"]

    # 2. Criando os caminhões com capacidades e horas de operação
    caminhao1 = Caminhao(id=1, capacidade=5000, horas_operacao=10, centro_distribuicao="Belém")
    caminhao2 = Caminhao(id=2, capacidade=6000, horas_operacao=8, centro_distribuicao="Recife")
    caminhao3 = Caminhao(id=3, capacidade=7000, horas_operacao=9, centro_distribuicao="São Paulo")
    caminhao4 = Caminhao(id=4, capacidade=8000, horas_operacao=12, centro_distribuicao="Curitiba")

    caminhoes = [caminhao1, caminhao2, caminhao3, caminhao4]

    # 3. Criando as entregas com destino, prazo e peso
    entrega1 = Entrega(destino="Recife", prazo_entrega="2024-11-20", peso=1500, prioridade=1)
    entrega2 = Entrega(destino="São Paulo", prazo_entrega="2024-11-18", peso=3000, prioridade=2)
    entrega3 = Entrega(destino="Curitiba", prazo_entrega="2024-11-15", peso=2000, prioridade=3)
    entrega4 = Entrega(destino="Belém", prazo_entrega="2024-11-22", peso=2500, prioridade=1)

    entregas = [entrega1, entrega2, entrega3, entrega4]

    # 4. Criando o grafo de rotas com as distâncias entre os centros de distribuição
    grafo = RotaGrafo()
    grafo.adicionar_rota("Belém", "Recife", -1.4558, -48.5044, -8.0476, -34.8770)
    grafo.adicionar_rota("Recife", "São Paulo", -8.0476, -34.8770, -23.5505, -46.6333)
    grafo.adicionar_rota("São Paulo", "Curitiba", -23.5505, -46.6333, -25.4284, -49.2733)
    grafo.adicionar_rota("Curitiba", "Recife", -25.4284, -49.2733, -8.0476, -34.8770)

    # 5. Instanciando o sistema logístico para otimização
    logistica = Logistica(centros, caminhoes, entregas, grafo)

    # 6. Alocando os caminhões de acordo com as entregas e o centro de distribuição mais próximo
    alocacao = logistica.alocar_caminhoes()

    # 7. Exibindo o resultado da alocação
    print("Alocação de Caminhões para as Entregas:")
    for entrega, caminhao in alocacao.items():
        print(f"Entrega para {entrega.destino} (Prazo: {entrega.prazo_entrega}, Peso: {entrega.peso}kg) - Alocada ao {caminhao}")

if __name__ == "__main__":
    main()
