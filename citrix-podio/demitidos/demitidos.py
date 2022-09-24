import pandas as pd
from dataframes import retorna_dados_dos_demitidos

dataframe_demitidos = pd.read_csv('demitidos.csv', dtype=str)
dataframe_demitidos = dataframe_demitidos.drop_duplicates(subset=['Nome Funcionários'], keep='first')


class Demitido(object):

    def __init__(self, nome=None, superior=None, dt_demissao=None, email_superior=None):
        self.nome = nome
        self.superior = superior
        self.dt_demissao = dt_demissao
        self.email_superior = email_superior

    @classmethod
    def verifica_demitido(cls, funcionario):
        nome, superior, dt_demissao, email_chefe = retorna_dados_dos_demitidos(funcionario)
        return cls(nome, superior, dt_demissao, email_chefe)

    def show_demitidos(self):
        return vars(self)


class Podio(object):

    def __init__(self, nome, patrimonios):
        self.nome = nome
        self.patrimonios = patrimonios

    @classmethod
    def retorna_dicionario_equipamento_colaborador(cls, colaborador):
        filtro = cls.client.Item.filter(24231717, {'filters': {203968038: colaborador, 203968026: [1]}})
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
            # Bloco de extração dos dígitos de patrimônio do DataFrame #
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
    output = pd.DataFrame()
    for _, row in dataframe_demitidos.iterrows():

        func_obj = Demitido.verifica_demitido(row['Nome Funcionários'])
        dict_a = func_obj.show_demitidos()
        eqpt = Podio.retorna_dicionario_equipamento_colaborador(func_obj.nome)
        dict_b = eqpt.show_podio()
        if dict_b['patrimonios'] != 'empty':
            new_dict = {**dict_a, **dict_b}
            print(new_dict)
    #         df_dictionary = pd.DataFrame([new_dict])
    #         output = pd.concat([output, df_dictionary], ignore_index=True)
    # print(output)


if __name__ == '__main__':
    iterar_dataframe()
