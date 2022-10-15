import pandas
import pandas as pd
from db_podio_conn import inicializa_cursor_sql_server
from queries import QUERY_TABLETS
import warnings

# Ignora alerta pelo uso de pyodbc pelo Pandas
warnings.filterwarnings('ignore')


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
    email_chefe = extrai_email_chefia(row)
    return nome, superior, dt_demissao, email_chefe


def extrai_email_chefia(row):
    """Inicializa Dataframe chefia e retorna email do chefe"""
    dataframe_atuais = pd.read_csv('atuais.csv', dtype=str)
    dataframe_chefia = dataframe_atuais[['NOMEFUNCIONARIO', 'EMAIL']].set_index('NOMEFUNCIONARIO'). \
        fillna('Sem e-mail cadastrado')
    # Atribui nome ao chefe e localiza o email do dataframe de funcionários ativos
    chefe = row['Nome Superior']
    email_chefe = dataframe_chefia.loc[chefe].to_dict('list')
    email_chefe = [val[0] for val in email_chefe.values()][0]
    return email_chefe


def sql_to_dataframe():
    conn = inicializa_cursor_sql_server()
    dataframe_from_sql = pandas.read_sql(QUERY_TABLETS, conn)
    print('Dataframe Montado')
    return dataframe_from_sql


if __name__ == '__main__':
    cursor = inicializa_cursor_sql_server()
    # query = retorna_listagem_tablets(conn)
    sql_to_dataframe()
