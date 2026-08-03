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
def gerar_estatisticas(df):

    print("\n===== ESTATÍSTICAS DESCRITIVAS =====")

    estatisticas = df.describe(include="all").T

    print(estatisticas)

    estatisticas.to_csv(
        "data/processed/estatisticas_descritivas.csv",
        encoding="utf-8-sig"
    )

    return estatisticas

# Criar uma tabela para fazer consultas com o sql 
def criar_banco(df, nome_banco):

    conn = sql.connect(nome_banco)

    df.to_sql(
        "funcionarios_clima",
        conn,
        if_exists="replace",
        index=False
    )

    cursor = conn.cursor()

    cursor.execute("""

    CREATE VIEW IF NOT EXISTS vw_satisfacao_area AS

    SELECT
    area,
    COUNT(*) AS total_colaboradores,
    ROUND(AVG(nivel_satisfacao),2) AS media_satisfacao,
    ROUND(AVG(recomendaria),2) AS media_recomendacao
FROM funcionarios_clima
GROUP BY area
ORDER BY media_satisfacao

    """)

    cursor.execute("""

    CREATE VIEW IF NOT EXISTS vw_cargos AS

    SELECT
        cargo,
        COUNT(*) AS total

    FROM funcionarios_clima

    GROUP BY cargo

    """)

    cursor.execute("""

    CREATE VIEW IF NOT EXISTS vw_tempo_empresa AS

    SELECT

        classificacao_experiencia,

        COUNT(*) AS total,

        ROUND(AVG(nivel_satisfacao),2) AS media_satisfacao

    FROM funcionarios_clima

    GROUP BY classificacao_experiencia
    ORDER BY media_satisfacao

    """)

    conn.commit()

    conn.close()
def resumo_executivo(df):

    print("\n===== RESUMO EXECUTIVO =====")

    print(f"Total colaboradores: {len(df)}")

    print(f"Satisfação média: {df['nivel_satisfacao'].mean():.2f}")

    print(f"Recomendação média: {df['recomendaria'].mean():.2f}")

    print()

    resumo = (

        df

        .groupby("area")

        .agg(

            Quantidade=("id_funcionario","count"),

            Media_Satisfacao=("nivel_satisfacao","mean"),

            Media_Indicaria=("recomendaria","mean")

        )

        .sort_values("Media_Satisfacao")

    )

    print(resumo)

    resumo.to_csv(

        "data/processed/resumo_area.csv",

        encoding="utf-8-sig"

    )

    return resumo
def exportar_dados(df):

    df.to_csv(

        "data/processed/base_tratada.csv",

        index=False,

        encoding="utf-8-sig"

    )

    print("CSV exportado.")



    
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

    gerar_estatisticas(df_clean)

    resumo_executivo(df_clean)

    exportar_dados(df_clean)

    criar_banco(
        df=df_clean,
        nome_banco="data/funcionarios.db"
    )

if __name__ == "__main__":
    main()