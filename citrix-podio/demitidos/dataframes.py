import pandas as pd
from db_podio_conn import inicializa_cursor_sql_server
from queries import QUERY_TABLETS
import warnings
import logging

# Ignora alerta pelo uso de pyodbc pelo Pandas
warnings.filterwarnings('ignore')

def sql_to_dataframe():
    conn = inicializa_cursor_sql_server()
    dataframe_from_sql = pd.read_sql(QUERY_TABLETS, conn)
    print('Dataframe Montado')
    return dataframe_from_sql


if __name__ == '__main__':
    cursor = inicializa_cursor_sql_server()
    # query = retorna_listagem_tablets(conn)
    sql_to_dataframe()
