from entity.rota import RotaGrafo


class CentroDistribuicao:
    _contador_id = 1

    def __init__(self, nome, id=None):
        self.id = id if id else CentroDistribuicao._gerar_id()
        self.nome = nome
        self.caminhoes = []
        self.rota_grafo = RotaGrafo()

    @classmethod
    def _gerar_id(cls):
        id_gerado = cls._contador_id
        cls._contador_id += 1
        return id_gerado

    def adicionar_caminhao(self, caminhao):
        self.caminhoes.append(caminhao)
        caminhao.centro = self
        print(f"Caminhão {caminhao.id} adicionado ao centro de distribuição {self.nome}.")

    def remover_caminhao(self, id_caminhao):
        for caminhao in self.caminhoes:
            if caminhao.id == id_caminhao:
                self.caminhoes.remove(caminhao)
                caminhao.centro = None
                print(f"Caminhão {caminhao.id} removido do centro de distribuição {self.nome}.")
                return
        print(f"Caminhão com ID {id_caminhao} não encontrado no centro {self.nome}.")

    def listar_caminhoes(self):
        if not self.caminhoes:
            print(f"Não há caminhões no centro de distribuição {self.nome}.")
        else:
            print(f"Caminhões no centro de distribuição {self.nome}:")
            for caminhao in self.caminhoes:
                print(caminhao)

    def buscar_caminhao_por_id(self, id_caminhao):
        for caminhao in self.caminhoes:
            if caminhao.id == id_caminhao:
                return caminhao
        print(f"Caminhão com ID {id_caminhao} não encontrado no centro {self.nome}.")
        return None


    def planejar_entrega(self, entrega):
        for caminhao in self.caminhoes:
            if caminhao.pode_transportar(entrega.peso):
                caminhao.adicionar_carga(entrega.peso)
                print(f"Entrega para {entrega.destino} atribuída ao caminhão {caminhao.id}.")
                distancia = self.rota_grafo.rota_mais_curta(self.nome, entrega.destino)
                if distancia is not None:
                    print(f"Rota mais curta para {entrega.destino}: {distancia} km.")
                    entrega.status = "Em trânsito"
                else:
                    print(f"Destino {entrega.destino} inacessível.")
                return
        print("Nenhum caminhão disponível para transportar esta entrega.")


    def __str__(self):
        return f"Centro: {self.nome}, ID: {self.id}, Caminhões: {len(self.caminhoes)}"
