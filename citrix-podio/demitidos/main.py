import pandas as pd
from demitidos import Demitido
from podio import Tablet
from db_local import get_entry
from dataframes import DATAFRAME_DEMITIDOS


def to_csv():
    df = pd.DataFrame()
    for _, row in DATAFRAME_DEMITIDOS.iterrows():
        demitido = Demitido.verifica_demitido(row['Nome Funcionários'])
        for entry in get_entry():
            equipamento = Tablet(*entry)
            if equipamento.utilizador == demitido.nome and equipamento.status == 'Com o colaborador':
                dicio = {'demitido': demitido.nome, 'dt_demissao': demitido.dt_demissao,
                         'patrimonio': equipamento.patrimonio, 'status': equipamento.status, 'email_chefe': demitido.
                        email_superior}
                df = df.append(dicio, ignore_index=True)
                df.to_csv('teste.csv', encoding='utf-8', index=False)
                print(df)
                # print(f'Demitido {demitido.nome} em {demitido.dt_demissao}  com equipamento de patrimônio: '
                #       f'{equipamento.patrimonio}, status: {equipamento.status}')

if __name__ == '__main__':
    to_csv()
