import pandas as pd




class Demitidos(object):

    def __init__(self):
        self.dataframe = pd.read_csv('Relatorio-demitidos.csv', dtype=str)

    def retorna_demitidos(self):

        lista_demitidos = self.dataframe.filter(items=['Nome Funcionários'], axis=1).apply(lambda x: x.astype(str)).\
            drop_duplicates(keep='first', inplace=False, subset=None)
        return lista_demitidos

