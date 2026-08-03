import pandas as pd
import numpy as np
import sqlite3 as sql


# ==========================
# IMPORTAÇÃO
# ==========================

def carregar_dados(caminho):

    if caminho.endswith(".csv"):
        df = pd.read_csv(caminho, encoding="utf-8")
    else:
        df = pd.read_excel(caminho)

    print("Dados importados com sucesso!")

    return df
df = carregar_dados("data/Avaliacao_de_Desempenho.csv")

def criar_banco(df, nome_banco):

    conn = sql.connect(nome_banco)

    df.to_sql(
        "funcionarios",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()
criar_banco(df,'data/desempenho.db')

