import pandas as pd
from pypodio2 import api

CLIENT_ID = ''
TOKEN = ''
USER = ''
PASSWORD = ''

dataframe_demitidos = pd.read_csv('Relatorio-demitidos.csv', dtype=str)
filtro_dataframe_demitidos = dataframe_demitidos.filter(items=['Nome Funcionários'], axis=1). \
    apply(lambda x: x.astype(str)). \
    drop_duplicates(keep='first', inplace=False, subset=None)


class Demitidos(object):

    def __init__(self, nome=None, superior=None, dt_demissao=None):
        self.nome = nome
        self.superior = superior
        self.dt_demissao = dt_demissao

    @classmethod
    def verifica_demitido(cls, funcionario):
        row = dataframe_demitidos.loc[dataframe_demitidos['Nome Funcionários'] == funcionario]
        dict_demitido = row[['Nome Funcionários', 'Nome Superior', 'Data Demissão']].to_dict('list')
        nome, superior, dt_demissao = [val[0] for val in dict_demitido.values()]
        return cls(nome, superior, dt_demissao)

    def __str__(self):
        return f'O funcionário {self.nome} foi demitido em {self.dt_demissao}. {self.superior}, favor realizar ' \
               f'a transferência'


class Podio(object):
    client = api.OAuthClient(CLIENT_ID, TOKEN, USER, PASSWORD)

    def __init__(self, nome, patrimonios):
        self.nome = nome
        self.patrimonios = patrimonios

    @staticmethod
    def inicializa_client():
        client = api.OAuthClient(CLIENT_ID, TOKEN, USER, PASSWORD)
        return client

    @classmethod
    def retorna_dicionario_equipamento_colaborador(cls, colaborador):

        filtro = cls.client.Item.filter(24231717, {'filters': {203968038: colaborador}})
        chave = []
        valor = []
        temp_tuple = []
        for key in filtro['items']:
            for i in key['fields']:
                for x, y in i.items():
                    chave.append(x)
                    valor.append(y)
        temp_tuple = list(zip(chave, valor))
        df = pd.DataFrame(temp_tuple, columns=['Campo', 'Valor'], dtype=str)
        codigos_de_patrimonio_do_dataframe = df.loc[df.shift(1)['Valor'] == 'Patrimônio']['Valor'] \
            .to_frame()
        dicionario_patrimonios_do_dataframe = codigos_de_patrimonio_do_dataframe.to_dict('records')

        # Bloco de extração dos dígitos de patrimônio do DataFrame
        c = 0
        novo_dicionario_de_patrimonios = {}
        while c < len(dicionario_patrimonios_do_dataframe):
            temp_dict = dicionario_patrimonios_do_dataframe[c]
            temp_list = []
            for value in temp_dict.values():
                for digit in value:
                    if digit.isdigit():
                        temp_list.append(digit)
                temp_list = ''.join(temp_list)
                novo_dicionario_de_patrimonios[f'Patrimônio: {c + 1}'] = temp_list
            c += 1

        return cls(colaborador, novo_dicionario_de_patrimonios)

    def show(self):
        return print(self.nome, self.patrimonios)




func = Podio.retorna_dicionario_equipamento_colaborador('')
func.show()


def iterar_dataframe():
    for _, row in dataframe_demitidos.iterrows():
        func = Demitidos.verifica_demitido(row['Nome Funcionários'])
        print(func)


if __name__ == '__main__':
    pass

#
#
#
#
#
#
# res = {key: dict_gigante[key] for key in dict_gigante.keys() & {'items'}}
# new_res = res['items'][0]
# new_dictão = {key: new_res[key] for key in new_res.keys() & {'fields'}}
# new_new_dictão = new_dictão['fields']
