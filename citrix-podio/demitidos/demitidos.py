import pandas as pd
from dataclasses import dataclass


@dataclass
class Demitido(object):
    nome: str
    superior: str
    dt_demissao: str
    email_superior: str = None

    @staticmethod
    def retorna_dados_dos_demitidos(demitido):
        """Inicializa Dataframe de demitidos e retorna os dados de identificação do demitido e seu chefe"""
        dataframe_demitidos = pd.read_csv('demitidos.csv', dtype=str)
        dataframe_demitidos = dataframe_demitidos.drop_duplicates(subset=['Nome Funcionários'], keep='first')
        # Filtra row por demitido do demitido e converte para dict
        row = dataframe_demitidos.loc[dataframe_demitidos['Nome Funcionários'] == demitido]
        dict_demitido = row[['Nome Funcionários', 'Nome Superior', 'Data Demissão']].to_dict('list')
        # Extrai valores do dict_demitido
        nome, superior, dt_demissao = [val[0] for val in dict_demitido.values()]
        # Chama função para retornar email do chefe do demitido
        email_chefe = Demitido.extrai_email_chefia(row)
        return Demitido(nome, superior, dt_demissao, email_chefe)

    @staticmethod
    def extrai_email_chefia(row):
        """Inicializa Dataframe chefia e retorna email do chefe"""
        dataframe_atuais = pd.read_csv('atuais2.csv', dtype=str)
        dataframe_chefia = dataframe_atuais[['NOMEFUNCIONARIO', 'EMAIL']].set_index('NOMEFUNCIONARIO'). \
            fillna(0)
        # Atribui nome ao chefe e localiza o email do dataframe de funcionários ativos
        try:
            chefe = row['Nome Superior']
            email_chefe = dataframe_chefia.loc[chefe].to_dict('list')
            email_chefe = [val[0] for val in email_chefe.values()][0]
            return email_chefe
        except Exception as err:
            f = open("erros.txt", "a")
            f.write(str(err))
            f.close()
            pass


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


if __name__ == '__main__':
    obj = Demitido.retorna_dados_dos_demitidos('ADRIANA FERRAZ DA SILVEIRA NERVETTI')
    print(obj)
