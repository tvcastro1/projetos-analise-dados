from pypodio2 import api, areas
from config_parser import get_api_keys
from dataclasses import dataclass


def inicializador_podio():
    client_id, client_secret, user, password = get_api_keys()
    client = api.OAuthClient(client_id, client_secret, user, password)
    return client


@dataclass
class Equipamento:
    patrimonio: str
    responsavel: str




if __name__ == '__main__':
    inicializador_podio()
    a = Equipamento('1', 'zé')
    print(a.patrimonio)
