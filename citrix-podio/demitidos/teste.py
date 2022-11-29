import sqlite3
import pandas as pd
from queries import QUERY_SELECT_ALL_TABLETS
#
# conn = sqlite3.connect('podio.db')
#
# sql_query = pd.read_sql_query('''
#                                SELECT
#                                *
#                                FROM tablets
#                                ''', conn)


# df_podio = pd.DataFrame(sql_query)
# df_demitidos = pd.read_csv('demitidos.csv', dtype=str).drop_duplicates()
#
# df_merged = pd.merge(df_podio, df_demitidos, how='inner', left_on='nome-colaborador', right_on='Nome Funcionários')
# df_merged_final = df_merged[df_merged.statusDesc == 'Com o colaborador']
# print(df_merged_final)

class DataManipulation(object):
    def __init__(self):
        self.df_demitidos = self.merged_df_demitidos_atuais_podio()
        self.df_podio = None

    @staticmethod
    def merged_df_demitidos_atuais_podio() -> pd.DataFrame:
        df_demitidos = DataManipulation.__csv_demitidos_para_df()
        df_atuais = DataManipulation.__csv_atuais_para_df()
        df_podio_tablets = DataManipulation.__sql_query_podio_tablets_para_df()
        df_merged_demitidos = pd.merge(df_demitidos, df_atuais, how='left', left_on='Nome Funcionários',
                                    right_on='NOMEFUNCIONARIO').fillna('None')
        df_merged_demitidos_podio_tablets = pd.merge(df_merged_demitidos, df_podio_tablets, how='inner',
                                                     left_on='Nome Funcionários', right_on='nome-colaborador')
        return df_merged_demitidos_podio_tablets

    @staticmethod
    def __csv_demitidos_para_df() -> pd.DataFrame:
        """Transforma csv Big/Demitdos em Dataframe"""
        big_demitidos = pd.read_csv('demitidos.csv', dtype=str)
        # Elimina duplicados e mantém primeiro registro
        big_demitidos = big_demitidos.drop_duplicates(subset=['Nome Funcionários'], keep='first')
        return big_demitidos

    @staticmethod
    def __csv_atuais_para_df() -> pd.DataFrame:
        """Inicializa dataframe atuais e retorna df"""
        big_atuais = pd.read_csv('atuais.csv', dtype=str)
        big_atuais = big_atuais[['NOMEFUNCIONARIO', 'EMAIL']].set_index('NOMEFUNCIONARIO'). \
            fillna(0)
        return big_atuais

    @staticmethod
    def __sql_query_podio_tablets_para_df() -> pd.DataFrame:
        conn = sqlite3.connect('podio.db')
        df_sql_query = pd.read_sql_query(QUERY_SELECT_ALL_TABLETS, conn)
        return df_sql_query

    def save_to_csv(self):
        self.df_demitidos.to_excel('dfteste.xlsx', encoding='utf-8')

if __name__ == '__main__':
    obj = DataManipulation()
    obj.save_to_csv()
    print(obj.df_demitidos)
    print('Fim da execução')
