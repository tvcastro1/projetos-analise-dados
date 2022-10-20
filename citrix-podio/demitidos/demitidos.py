import pandas as pd
from dataframes import retorna_dados_dos_demitidos
from dataclasses import dataclass


@dataclass
class Demitido(object):
    nome: str
    superior: str
    dt_demissao: str
    email_superior: str = None

    @classmethod
    def verifica_demitido(cls, funcionario):
        nome, superior, dt_demissao, email_superior = retorna_dados_dos_demitidos(funcionario)
        return cls(nome, superior, dt_demissao, email_superior)

