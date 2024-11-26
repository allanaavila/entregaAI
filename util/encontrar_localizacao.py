from opencage.geocoder import OpenCageGeocode
from dotenv import load_dotenv
from typing import Any
import os

load_dotenv()
chave_api = os.getenv("OPENCAGE_API_KEY")

def obter_coordenadas_opencage(logradouro: str, cidade: str, estado: str) -> tuple[float, float] | dict[str, str]:
    """
    Consulta a latitude e longitude de um endereço usando a API do OpenCage.
    :param logradouro: Logradouro (string).
    :param cidade: Cidade (string).
    :param estado: Estado (string).
    :return: Tupla com latitude e longitude, respectivamente.
    """
    try:
        endereco = f"{logradouro}, {cidade}, {estado}, Brasil"
        geocoder = OpenCageGeocode(chave_api)
        resultado = geocoder.geocode(endereco)

        if resultado:
            coordenadas = resultado[0]['geometry']
            return coordenadas['lat'], coordenadas['lng']
        else:
            return {"erro": "Endereço não encontrado."}
    except Exception as e:
        return {"erro": str(e)}