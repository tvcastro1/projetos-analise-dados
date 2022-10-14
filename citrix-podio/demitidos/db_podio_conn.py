import pyodbc


def inicializa_cursor_sql_server():
    """
    Realiza conexão ao Sql Server
    :return: pyodbc connection
    """
    server = ''
    database = ''
    username = ''
    authentication = 'ActiveDirectoryInteractive'
    driver = '{ODBC Driver 18 for SQL Server}'
    try:
        conn = pyodbc.connect('DRIVER=' + driver +
                              ';SERVER=' + server +
                              ';PORT=1433;DATABASE=' + database +
                              ';UID=' + username +
                              ';AUTHENTICATION=' + authentication)
        cursor = conn.cursor()
        return conn

    except pyodbc.Error as ex:
        print(f'Erro de Conexão:{ex.args[1]}')


# def retorna_listagem_tablets(cursor):
#     query_tablets = """SELECT [nome-colaborador]
#     ,[patrimonio-novo]
#     ,[last_event_on]
#     FROM [Podio].[ListarTabletsNovos] a
#     WHERE [last_event_on] = (SELECT MAX(last_event_on) FROM [Podio].[ListarTabletsNovos]
#     WHERE app_item_id = a.app_item_id)
#     ORDER BY [nome-colaborador] ASC"""
#
#     retorno_query_tablets = cursor.execute(query_tablets)
#     return retorno_query_tablets


# cursor.execute(query_tablets)
# results = cursor.fetchall()
# print(results)


if __name__ == '__main__':
    pass
    # cursor = inicializa_cursor_sql_podio()
    # retorna_listagem_tablets(cursor)
