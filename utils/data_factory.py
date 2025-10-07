from faker import Faker
import random
from utils.catalogo import (
    catalogo, tipos_bodega, Tipo_Estandar,
    tipos_calle, letras, bis, cuadrantes, sufijos
)

faker = Faker("es")

class DataFactory:

    @staticmethod
    def generar_direccion():
        direccion = {
            "tipo_calle": random.choice(tipos_calle),
            "numero_principal": str(random.randint(1, 150)),
            "letra_principal": random.choice(letras),
            "prefijo_bis": random.choice(bis),
            "numero_secundaria": str(random.randint(1, 150)),
            "letra_secundaria": random.choice(letras),
            "sufijo": random.choice(sufijos),
            "cuadrante": random.choice(cuadrantes),
            "numero_complementario": str(random.randint(1, 100)),
            "complemento": faker.sentence(nb_words=3)
        }
        return direccion

   

    @staticmethod
    def generar_bodega():
        pais = random.choice(list(catalogo.keys()))
        departamento = random.choice(list(catalogo[pais].keys()))
        ciudad = random.choice(catalogo[pais][departamento])

        tipo_bodega = random.choice(tipos_bodega)
        tipo_estandar = random.choice(Tipo_Estandar)
        direccion_detallada = DataFactory.generar_direccion()

        return {
            "nombre_bodega": f"Bodega_{faker.company()}_{faker.random_int(100,999)}",
            "codigo_bodega": f"BOD{faker.random_int(1000,9999)}",
            "pais": pais,
            "departamento": departamento,
            "ciudad": ciudad,
            "tipo_bodega": tipo_bodega,
            "modulos": random.randint(1, 10),
            "pisos": random.randint(1, 5),
            "estantes": random.randint(5, 50),
            "entrepaños": random.randint(1, 100),
            "capacidad": random.randint(1, 100),
            "tipo_estandar": tipo_estandar,
            "direccion_detallada": direccion_detallada
        }
