from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from dotenv import load_dotenv
import os

os.environ.pop("NOMINATIM_USER_AGENT", None)
load_dotenv(override=True)
NOMINATIM_USER_AGENT = os.getenv("NOMINATIM_USER_AGENT", "default_user_agent")

class CalcularDistancia:
    def __init__(self):
        self.__user_agent = NOMINATIM_USER_AGENT
        self.geolocator = Nominatim(user_agent=self.__user_agent)

    def obter_coordenadas(self, endereco):
        try:
            local = self.geolocator.geocode(endereco)
            if local is None:
                print(f"Erro: Não foi possível encontrar o endereço: {endereco}")
                return None, None
            return local.latitude, local.longitude
        except Exception as e:
            print(f"Erro ao geolocalizar o endereço {endereco}: {e}")
            return None, None

    def calcular_distancia(self, endereco_inicial, endereco_final):
        latitude_inicial, longitude_inicial = self.obter_coordenadas(endereco_inicial)
        latitude_final, longitude_final = self.obter_coordenadas(endereco_final)

        if None in [latitude_inicial, longitude_inicial, latitude_final, longitude_final]:
            return None

        distancia = geodesic((latitude_inicial, longitude_inicial), (latitude_final, longitude_final)).kilometers
        print(f"Distância inicial: {distancia:.2f} km")

        distancia = self.ajustar_distancia(distancia)

        return distancia

    def ajustar_distancia(self, distancia):
        if distancia < 300:
            return distancia * 1.44
        elif 301 <= distancia <= 999:
            return distancia * 1.3
        elif distancia >= 1000:
            return distancia * 1.4
        return distancia

