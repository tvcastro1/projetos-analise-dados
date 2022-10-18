from pypodio2 import api, areas
from config_parser import get_api_keys
from db_local import get_entry
from dataclasses import dataclass


def inicializador_podio():
    client_id, client_secret, user, password = get_api_keys()
    client = api.OAuthClient(client_id, client_secret, user, password)
    return client


@dataclass
class Tablet(object):
    item_id: int
    imei: str
    patrimonio: str
    modelo: str
    serie: str
    tipo: str
    utilizador: str
    sistema: str
    status: str
    last_event: str


# for list in get_entry():
#     myinst = Tablet(*list)
#     print(myinst)

    # @dataclass

# class Ativo(object):
#     id: int
#     departamento: str
#     status: str
#     tipo: str
#     utilizador: str
#     modelo: str
#
# @dataclass
# class Tablet(Ativo):


if __name__ == '__main__':
    pass
