import pyodbc


def inicializa_cursor():
    server = ''
    database = ''
    username = ''
    authentication = ''
    driver = ''
    try:
        conn = pyodbc.connect('DRIVER=' + driver +
                              ';SERVER=' + server +
                              ';PORT=1433;DATABASE=' + database +
                              ';UID=' + username +
                              ';AUTHENTICATION=' + authentication)
        cursor = conn.cursor()
        return cursor
    except pyodbc.Error as ex:
        print(f'Erro de Conexão:{ex.args[1]}')


def retorna_listagem_tablets(cursor):
    query_tablets = """SELECT [nome-colaborador]
    ,[patrimonio-novo]
    ,[last_event_on]
    FROM [Podio].[ListarTabletsNovos] a
    WHERE [last_event_on] = (SELECT MAX(last_event_on) FROM [Podio].[ListarTabletsNovos]
    WHERE app_item_id = a.app_item_id)
    AND [status] = 1"""

    retorno_query_tablets = cursor.execute(query_tablets)
    return retorno_query_tablets


# cursor.execute(query_tablets)
# results = cursor.fetchall()
# print(results)


if __name__ == '__main__':
    cursor = inicializa_cursor()
    retorna_listagem_tablets(cursor)
