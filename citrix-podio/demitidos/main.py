import pandas as pd
from demitidos import Demitido
from podio import Tablet
from db_local import get_entry
from emailer import email_sender

DATAFRAME_DEMITIDOS = pd.read_csv('demitidos.csv', dtype=str).drop_duplicates(subset=['Nome Funcionários'], keep='first')

def to_csv():
    df = pd.DataFrame()
    for _, row in DATAFRAME_DEMITIDOS.iterrows():
        demitido = Demitido.retorna_dados_dos_demitidos(row['Nome Funcionários'])
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


def to_email():
    x = 0
    df = pd.DataFrame()
    for _, row in DATAFRAME_DEMITIDOS.iterrows():
        demitido = Demitido.verifica_demitido(row['Nome Funcionários'])
        for entry in get_entry():
            equipamento = Tablet(*entry)
            if equipamento.utilizador == demitido.nome and equipamento.status == 'Com o colaborador' \
                    and demitido.email_superior is not None:
                dicio = {'demitido': demitido.nome, 'dt_demissao': demitido.dt_demissao,
                         'patrimonio': equipamento.patrimonio, 'status': equipamento.status, 'email_chefe': demitido.
                        email_superior}
                email_sender(demitido.email_superior, demitido.superior, demitido.nome, demitido.dt_demissao,
                             equipamento.modelo, equipamento.patrimonio)


if __name__ == '__main__':
    to_csv()
