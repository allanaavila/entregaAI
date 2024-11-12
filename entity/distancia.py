import math

class Distancia:
    def __init__(self, lat1, lon1, lat2, lon2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2

    def calcular_distancia(self):
        lat1_rad = math.radians(self.lat1)
        lon1_rad = math.radians(self.lon1)
        lat2_rad = math.radians(self.lat2)
        lon2_rad = math.radians(self.lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        raio_terra_km = 6371

        distancia_km = raio_terra_km * c
        return distancia_km

    def __str__(self):
        return f"Distância entre ({self.lat1}, {self.lon1}) e ({self.lat2}, {self.lon2}): {self.calcular_distancia()} km"