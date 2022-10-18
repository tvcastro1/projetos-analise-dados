from demitidos import Demitido
from podio import Tablet
import pandas as pd
import csv
from db_local import get_entry
from dataframes import retorna_dados_dos_demitidos

dataframe_demitidos = pd.read_csv('demitidos.csv', dtype=str)
dataframe_demitidos = dataframe_demitidos.drop_duplicates(subset=['Nome Funcionários'], keep='first')


def demitido_init():
    total = 0
    csv_header = ['nome','dt_demissao','patrimonio']

    for _, row in dataframe_demitidos.iterrows():
        temp_list = []
        demitido = Demitido.verifica_demitido(row['Nome Funcionários'])
        b = demitido.show_demitidos()
        z = b['dt_demissao']
        b = b['nome']

        for list in get_entry():
            myinst = Tablet(*list)
            a = myinst.utilizador
            c = myinst.patrimonio
            y = myinst.status
            if a == b and y == 'Com o colaborador':
                # temp_list.append(b)
                # temp_list.append(z)
                # temp_list.append(c)
                # with open('students.csv', 'w',newline='') as file:
                #     writer = csv.writer(file, delimiter=",")
                #     writer.writerow(csv_header)
                #     # Use writerows() not writerow()
                #     for linha in temp_list:
                #         columns = [c.strip() for c in linha.strip(', ').split(',')]
                #         writer.writerow(columns)
                #     writer.writerow(temp_list)

                print(f'Demitido {b} em {z}  com equipamento de patrimônio: {c}, status: {y}' )


                total += 1
    print(total)


demitido_init()
