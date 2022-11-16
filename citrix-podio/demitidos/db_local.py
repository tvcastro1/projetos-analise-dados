import sqlite3
from sqlite3 import Error
import pandas as pd
from dataframes import sql_to_dataframe

DB_FILE_PATH = 'podio.db'


def connect_to_db(db_file):
    """
    Conecta em uma base SQlite, se o bd não existe ele será criado
    :param db_file: caminho relativo ou absoluto da base
    :return: sqlite3 connection
    """
    sqlite3_conn = None

    try:
        sqlite3_conn = sqlite3.connect(db_file)
        return sqlite3_conn

    except Error as err:
        print(err)

        if sqlite3_conn is not None:
            sqlite3_conn.close()


def insert_values_to_table(table_name):
    """
    Insere valores de um dataframe em uma tabela do Sqlite
    :param table_name: table name in the database to insert the data into
    :return: None
    """

    conn = connect_to_db(DB_FILE_PATH)

    if conn is not None:
        c = conn.cursor()

        # Create table if it is not exist
        c.execute('CREATE TABLE IF NOT EXISTS ' + table_name +
                  '([app_item_id]        INTEGER,'
                  '[imei]            TEXT,'
                  '[patrimonio-novo]      TEXT,'
                  '[modeloDesc]          TEXT,'
                  '[serie]           TEXT,'
                  '[tipo-de-dispositivoDesc]       TEXT,'
                  '[nome-colaborador]       TEXT,'
                  '[sistema-utilizadoDesc]      TEXT,'
                  '[statusDesc]     TEXT,'
                  '[last_event_on]          TEXT)')
        df = sql_to_dataframe()

        # df.columns = get_column_names_from_db_table(c, table_name)

        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)

        conn.close()
        print('SQL insert process finished')
    else:
        print('Connection to database failed')


def get_entry():

    conn = connect_to_db(DB_FILE_PATH)
    if conn is not None:
        c = conn.cursor()

        c.execute("SELECT * FROM tablets")
        results = c.fetchone()
        yield results
    else:
        print('Falha na conexão ao banco de dados')



if __name__ == '__main__':
    for row in get_entry():
        print(row)

