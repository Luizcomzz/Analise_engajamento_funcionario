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


# ==========================
# TRATAMENTO
# ==========================

def tratar_dados(df):

    df = df.copy()

    # Padronização dos nomes
    df.columns = df.columns.str.lower().str.strip()

    df = df.rename(columns={
        "aval_valores": "avaliacao_valores",
        "aval_performace": "avaliacao_performance",
        "aval_equipe": "avaliacao_equipe",
        "desc_satisfacao": "descricao_satisfacao",
        "desc_recomendaria": "descricao_recomendaria",
        "class_experiencia": "classificacao_experiencia"
    })

    # =====================
    # Classificação das variáveis
    # =====================

    qualitativas_ordinais = [
        "avaliacao_valores",
        "avaliacao_performance",
        "avaliacao_equipe",
        "faixa_idade",
        "descricao_satisfacao",
        "descricao_recomendaria",
        "classificacao_experiencia"
    ]

    qualitativas_nominais = [
        "apelido",
        "area",
        "cargo"
    ]

    quantitativas_discretas = [
        "id_funcionario",
        "idade",
        "nivel_satisfacao",
        "recomendaria"
    ]

    quantitativas_continuas = [
        "anos_na_empresa"
    ]

    classificacao = {}

    for coluna in qualitativas_ordinais:
        classificacao[coluna] = "Qualitativa ordinal"

    for coluna in qualitativas_nominais:
        classificacao[coluna] = "Qualitativa nominal"

    for coluna in quantitativas_discretas:
        classificacao[coluna] = "Quantitativa discreta"

    for coluna in quantitativas_continuas:
        classificacao[coluna] = "Quantitativa contínua"

    # =====================
    # Tabela resumo
    # =====================

    tabela_variaveis = pd.DataFrame({

        "variavel": df.columns,

        "tipo_inicial_pandas": [
            str(df[c].dtype)
            for c in df.columns
        ],

        "classificacao_estatistica": [
            classificacao.get(c, "Não classificada")
            for c in df.columns
        ],

        "valores_distintos": [
            df[c].nunique(dropna=True)
            for c in df.columns
        ],

        "exemplos": [

            df[c]
            .dropna()
            .drop_duplicates()
            .head(3)
            .tolist()

            for c in df.columns

        ]

    })

    print("\n===== CLASSIFICAÇÃO DAS VARIÁVEIS =====")
    print(tabela_variaveis)

    # =====================
    # Limpeza
    # =====================

    colunas_textuais = df.select_dtypes(
        include=["object", "string"]
    ).columns

    df[colunas_textuais] = df[colunas_textuais].apply(
        lambda coluna: coluna.str.strip()
    )

    marcadores_invalidos = [
        "?",
        "",
        "NA",
        "N/A",
        "null",
        "None"
    ]

    df[colunas_textuais] = df[colunas_textuais].replace(
        marcadores_invalidos,
        np.nan
    )

    linhas_antes = len(df)

    df_clean = df.dropna().copy()

    # =====================
    # Conversão de tipos
    # =====================

    df_clean[quantitativas_discretas] = (
        df_clean[quantitativas_discretas]
        .astype("int64")
    )

    for coluna in quantitativas_continuas:

     df_clean[coluna] = (
          df_clean[coluna]
          .astype(str)
         .str.replace(",", ".", regex=False)
         .astype(float)
     )

    df_clean[qualitativas_nominais] = (
        df_clean[qualitativas_nominais]
        .astype("category")
    )

    linhas_depois = len(df_clean)

    print("\n===== LIMPEZA =====")

    print(f"Linhas antes : {linhas_antes}")
    print(f"Linhas depois: {linhas_depois}")
    print(f"Linhas removidas: {linhas_antes-linhas_depois}")
    print(f"Percentual removido: {100*(linhas_antes-linhas_depois)/linhas_antes:.2f}%")

    print("\n===== TIPOS FINAIS =====")

    print(df_clean.dtypes)

    print(
        "\nPossui valores ausentes?",
        df_clean.isna().any().any()
    )

    return df_clean

# Criar uma tabela para fazer consultas com o sql 
def criar_banco(df, nome_banco):

    conn = sql.connect(nome_banco)

    df.to_sql(
        "funcionarios",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

# ==========================
# MAIN
# ==========================

def main():

    df = carregar_dados("data/Pesquisa_de_Clima.csv")

    print("\n===== INFORMAÇÕES =====")
    df.info()

    print("\n===== ESTATÍSTICAS =====")
    print(df.describe(include="all").T)

    print("\n===== PRIMEIRAS LINHAS =====")
    print(df.head())

    df_clean = tratar_dados(df)

    criar_banco(
        df = df_clean,
        nome_banco="data/funcionarios.db"
    )

    print("Pipeline executado com sucesso!")


if __name__ == "__main__":
    main()