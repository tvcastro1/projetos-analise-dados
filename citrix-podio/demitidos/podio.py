# from pypodio2 import api
# from config_parser import get_api_keys
from dataclasses import dataclass


# def inicializador_podio():
#     client_id, client_secret, user, password = get_api_keys()
#     client = api.OAuthClient(client_id, client_secret, user, password)
#     return client


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





# class Podio(object):
#
#     def __init__(self, nome, patrimonios):
#         self.nome = nome
#         self.patrimonios = patrimonios
#
#     @classmethod
#     def retorna_dicionario_equipamento_colaborador(cls, colaborador):
#         filtro = cls.client.Item.filter(24231717, {'filters': {203968038: colaborador, 203968026: [1]}})
#         if filtro['filtered'] > 0:
#             chave = []
#             valor = []
#             temp_tuple = []
#             for key in filtro['items']:
#                 for i in key['fields']:
#                     for x, y in i.items():
#                         chave.append(x)
#                         valor.append(y)
#             temp_tuple = list(zip(chave, valor))
#             df = pd.DataFrame(temp_tuple, columns=['Campo', 'Valor'], dtype=str)
#             codigos_de_patrimonio_do_dataframe = df.loc[df.shift(1)['Valor'] == 'Patrimônio']['Valor'] \
#                 .to_frame()
#             dicionario_patrimonios_do_dataframe = codigos_de_patrimonio_do_dataframe.to_dict('records')
#             # Bloco de extração dos dígitos de patrimônio do DataFrame #
#             c = 0
#             novo_dicionario_de_patrimonios = {}
#             lista_patrimonios = []
#             while c < len(dicionario_patrimonios_do_dataframe):
#                 temp_dict = dicionario_patrimonios_do_dataframe[c]
#                 temp_list = []
#                 for value in temp_dict.values():
#                     for digit in value:
#                         if digit.isdigit():
#                             temp_list.append(digit)
#                     temp_list = ''.join(temp_list)
#                     lista_patrimonios.append(temp_list)
#                 c += 1
#             return cls(colaborador, lista_patrimonios)
#         else:
#             return cls(colaborador, 'empty')
#
#     def show_podio(self):
#         try:
#             return vars(self)
#         except AttributeError:
#             pass
#
# def monta_obj():
#     for lista in get_entry():
#         myinst = Tablet(*lista)
#         yield myinst
#
# obj = monta_obj()
# print(obj)

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
