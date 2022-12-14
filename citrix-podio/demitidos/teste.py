import sqlite3
import pandas as pd
from queries import QUERY_SELECT_ALL_TABLETS


class DataframeDemitidos(object):
    dataframe_demitidos_s_filtro = pd.DataFrame()

    @classmethod
    def carrega_df_demitidos(cls):
        df_demitidos = cls.__csv_demitidos_para_df()
        df_atuais = cls.__csv_atuais_para_df()
        df_podio_tablets = cls.__sql_query_podio_tablets_para_df()
        # Bloco de Merge
        df_merged_demitidos = pd.merge(df_demitidos, df_atuais, how='left', left_on='Nome Superior',
                                       right_on='NOMEFUNCIONARIO', indicator=True)
        df_merged_demitidos_podio_tablets = pd.merge(df_merged_demitidos, df_podio_tablets, how='inner',
                                                     left_on='Nome Funcionários', right_on='nome-colaborador')
        df_merged_demitidos_podio_tablets.drop_duplicates(subset=['patrimonio-novo'], keep='first', inplace=True)
        df_merged_demitidos_podio_tablets = df_merged_demitidos_podio_tablets[['Nome Funcionários', 'Data Demissão',
                                                                               'Nome Superior', 'EMAIL',
                                                                               'patrimonio-novo', 'modeloDesc',
                                                                               'statusDesc']]
        # Bloco de tratamento de cabeçalho do DF
        df_merged_demitidos_podio_tablets = df_merged_demitidos_podio_tablets.rename(
            columns={'Nome Funcionários': 'nome_funcionarios', 'Data Demissão': 'data_demissao',
                     'Nome Superior': 'nome_superior',
                     'EMAIL': 'email', 'patrimonio-novo': 'patrimonio_novo', 'modeloDesc': 'modelo_desc',
                     'statusDesc': 'status_desc'})
        cls.dataframe_demitidos_s_filtro = df_merged_demitidos_podio_tablets.fillna('null')
        return cls

    @staticmethod
    def __csv_demitidos_para_df() -> pd.DataFrame:
        """Transforma csv Big/Demitdos em Dataframe"""
        big_demitidos = pd.read_csv('demitidos.csv', dtype=str)
        # Elimina duplicados e mantém primeiro registro
        big_demitidos = big_demitidos.drop_duplicates(subset=['Nome Funcionários'], keep='first')
        return big_demitidos

    @staticmethod
    def __csv_atuais_para_df() -> pd.DataFrame:
        """Parsing de funcionários atuais para DF"""
        big_atuais = pd.read_csv('atuais.csv', dtype=str)
        big_atuais = big_atuais[['NOMEFUNCIONARIO', 'EMAIL']]
        return big_atuais

    @staticmethod
    def __sql_query_podio_tablets_para_df() -> pd.DataFrame:
        """Parsing sql query Podio para DF"""
        conn = sqlite3.connect('podio.db')
        df_sql_query = pd.read_sql_query(QUERY_SELECT_ALL_TABLETS, conn)
        return df_sql_query

    @staticmethod
    def salva_para_xlsx(dataframe=None) -> None:
        dataframe.to_excel('demitidos_s_chefe.xlsx', encoding='utf-8')
        return None

    def __init__(self):
        self.df_concat = None
        self.df_demitidos_sem_chefia = None

    def group_concat_df(self):
        # self.df_concat = self.dataframe_demitidos_s_filtro.query("status_desc == 'Com o colaborador'")
        self.df_concat = self.dataframe_demitidos_s_filtro.groupby(['nome_funcionarios'], as_index=False).agg(
            {'patrimonio_novo': ', '.join})
        self.salva_para_xlsx(self.df_concat)

    def df_sem_chefia(self):
        df = self.dataframe_demitidos_s_filtro.query("nome_superior != 'null'")
        self.salva_para_xlsx(df)
        self.df_demitidos_sem_chefia = df

        print(df)

    def __str__(self) -> str:
        return self.df_demitidos_sem_chefia.to_string()


if __name__ == '__main__':
    df = DataframeDemitidos.carrega_df_demitidos()
    obj = DataframeDemitidos()
    obj.group_concat_df()
    obj.df_sem_chefia()

    # obj = DataframeDemitidos()
    # obj.save_to_csv()
    # print(obj.df_demitidos)
    # print('Fim da execução')
