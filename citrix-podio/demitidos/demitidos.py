import pandas as pd
from pypodio2 import api

CLIENT_ID = 'tablets-novo'
TOKEN = '91zyXWNRsI0lXjpBZIaBknYUlNWlZSKVSBc7LG9thJrQY3ve7MVtxWptgMdM1Xje'
USER = 'vieira.thiago@parceiro.mrv.com.br'
PASSWORD = 'N3R@tkvP'

dataframe_demitidos = pd.read_csv('demitidos.csv', dtype=str)
dataframe_demitidos = dataframe_demitidos.drop_duplicates(subset=['Nome Funcionários'],keep='first')
filtro_dataframe_demitidos = dataframe_demitidos.filter(items=['Nome Funcionários'], axis=1). \
    apply(lambda x: x.astype(str)). \
    drop_duplicates(keep='first', inplace=False, subset=None)

dataframe_atuais = pd.read_csv('atuais.csv', dtype=str)

dataframe_chefia = dataframe_atuais[['NOMEFUNCIONARIO', 'EMAIL']].set_index('NOMEFUNCIONARIO').\
    fillna('Sem e-mail cadastrado')


class Demitidos(object):

    def __init__(self, nome=None, superior=None, dt_demissao=None, email_superior=None):
        self.nome = nome
        self.superior = superior
        self.dt_demissao = dt_demissao
        self.email_superior = email_superior

    @classmethod
    def verifica_demitido(cls, funcionario):
        row = dataframe_demitidos.loc[dataframe_demitidos['Nome Funcionários'] == funcionario]
        dict_demitido = row[['Nome Funcionários', 'Nome Superior', 'Data Demissão']].to_dict('list')
        nome, superior, dt_demissao = [val[0] for val in dict_demitido.values()]
        chefe = row['Nome Superior']
        email_chefe = dataframe_chefia.loc[chefe].to_dict('list')
        email_chefe = [val[0] for val in email_chefe.values()][0]
        return cls(nome, superior, dt_demissao, email_chefe)

    @property
    def email_chefia(self):
        return self._email_superior

    @email_chefia.setter
    def email_chefia(self, email):
        self._email_superior = email

    def show_demitidos(self):
        return vars(self)
    # def __str__(self):
    #     return f'O funcionário {self.nome} foi demitido em {self.dt_demissao}. {self.superior}, favor realizar ' \
    #            f'a transferência e seu email é {self._email_superior}'


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
        filtro = cls.client.Item.filter(24231717, {'filters': {203968038: colaborador, 203968026:[1]}})
        if filtro['filtered'] > 0:
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
            #### Bloco de extração dos dígitos de patrimônio do DataFrame ####
            c = 0
            novo_dicionario_de_patrimonios = {}
            lista_patrimonios = []
            while c < len(dicionario_patrimonios_do_dataframe):
                temp_dict = dicionario_patrimonios_do_dataframe[c]
                temp_list = []
                for value in temp_dict.values():
                    for digit in value:
                        if digit.isdigit():
                            temp_list.append(digit)
                    temp_list = ''.join(temp_list)
                    lista_patrimonios.append(temp_list)
                c += 1
            return cls(colaborador, lista_patrimonios)
        else:
            return cls(colaborador, 'empty')

    def show_podio(self):
        try:
            return vars(self)
        except AttributeError:
            pass

def iterar_dataframe():
    for _, row in dataframe_demitidos.iterrows():
        func_obj = Demitidos.verifica_demitido(row['Nome Funcionários'])
        dict_a = func_obj.show_demitidos()
        eqpt = Podio.retorna_dicionario_equipamento_colaborador(func_obj.nome)
        dict_b = eqpt.show_podio()
        if dict_b['patrimonios'] != 'empty':
            new_dict = {**dict_a, **dict_b}
            print(new_dict)



def monta_funcionario_demitido(row):
    func_obj = Demitidos.verifica_demitido(row['Nome Funcionários'])
    return print(func_obj)

def email_superior_override(row):
    chefe = row['Nome Superior']
    email_chefe = dataframe_chefia.loc[chefe]
    setter = Demitidos()
    setter.email_chefia(email_chefe)
    return



# def compara_dataframe_demitidos_atuais(chefe):
#     return dataframe_chefia.loc[chefe]

if __name__ == '__main__':
    iterar_dataframe()


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
