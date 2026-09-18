import os
import sqlite3
import pandas as pd
import numpy as np


# ================================================================
# Constantes — caminhos centralizados para fácil manutenção
# ================================================================
RAW_CLIMA    = "data/Pesquisa_de_Clima.csv"
DB_PATH      = "data/funcionarios.db"
OUT_STATS    = "data/processed/estatisticas_descritivas.csv"
OUT_RESUMO   = "data/processed/resumo_area.csv"
OUT_TRATADA  = "data/processed/base_tratada.csv"


# ================================================================
# IMPORTAÇÃO
# ================================================================

def carregar_dados(caminho: str) -> pd.DataFrame:
    """
    Lê um arquivo CSV ou Excel e retorna um DataFrame.

    Parâmetros:
        caminho (str): Caminho para o arquivo de dados.

    Retorna:
        pd.DataFrame: Dados carregados.

    Lança:
        FileNotFoundError: Se o arquivo não existir.
    """
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")

    if caminho.endswith(".csv"):
        df = pd.read_csv(caminho, encoding="utf-8")
    else:
        df = pd.read_excel(caminho)

    print(f"Dados importados com sucesso! ({len(df)} registros)")
    return df


# ================================================================
# TRATAMENTO
# ================================================================

def _renomear_colunas(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza nomes de colunas para snake_case e aplica renomeações."""
    df.columns = df.columns.str.lower().str.strip()
    return df.rename(columns={
        "aval_valores"    : "avaliacao_valores",
        "aval_performace" : "avaliacao_performance",
        "aval_equipe"     : "avaliacao_equipe",
        "desc_satisfacao" : "descricao_satisfacao",
        "desc_recomendaria": "descricao_recomendaria",
        "class_experiencia": "classificacao_experiencia"
    })


def _limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços, substitui marcadores inválidos por NaN e dropa nulos."""
    colunas_textuais = df.select_dtypes(include=["object", "string"]).columns
    df[colunas_textuais] = df[colunas_textuais].apply(lambda col: col.str.strip())

    marcadores_invalidos = ["?", "", "NA", "N/A", "null", "None"]
    df[colunas_textuais] = df[colunas_textuais].replace(marcadores_invalidos, np.nan)

    linhas_antes  = len(df)
    df_clean      = df.dropna().copy()
    linhas_depois = len(df_clean)

    print(f"\n--- Limpeza ---")
    print(f"Linhas antes        : {linhas_antes}")
    print(f"Linhas depois       : {linhas_depois}")
    print(f"Linhas removidas    : {linhas_antes - linhas_depois}")
    print(f"Percentual removido : {100 * (linhas_antes - linhas_depois) / linhas_antes:.2f}%")

    return df_clean


def _converter_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """Converte colunas para os tipos estatísticos corretos."""
    quantitativas_discretas  = ["id_funcionario", "idade", "nivel_satisfacao", "recomendaria"]
    quantitativas_continuas  = ["anos_na_empresa"]
    qualitativas_nominais    = ["apelido", "area", "cargo"]

    df[quantitativas_discretas] = df[quantitativas_discretas].astype("int64")

    for coluna in quantitativas_continuas:
        df[coluna] = (
            df[coluna]
            .astype(str)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

    df[qualitativas_nominais] = df[qualitativas_nominais].astype("category")

    print("\n--- Tipos finais ---")
    print(df.dtypes)

    return df


def tratar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Orquestra o pipeline de tratamento: renomeia, limpa e converte tipos.

    Parâmetros:
        df (pd.DataFrame): DataFrame bruto carregado do CSV.

    Retorna:
        pd.DataFrame: DataFrame limpo e tipado corretamente.
    """
    df = df.copy()
    df = _renomear_colunas(df)
    df = _limpar_dados(df)
    df = _converter_tipos(df)
    return df


# ================================================================
# ANÁLISE E EXPORTAÇÃO
# ================================================================

def gerar_estatisticas(df: pd.DataFrame) -> pd.DataFrame:
    """Gera estatísticas descritivas e salva em CSV."""
    print("\n--- Estatísticas Descritivas ---")
    estatisticas = df.describe(include="all").T
    print(estatisticas)
    estatisticas.to_csv(OUT_STATS, encoding="utf-8-sig")
    return estatisticas


def resumo_executivo(df: pd.DataFrame) -> pd.DataFrame:
    """Gera resumo por área com satisfação e recomendação médias."""
    print("\n--- Resumo Executivo ---")
    print(f"Total colaboradores : {len(df)}")
    print(f"Satisfação média    : {df['nivel_satisfacao'].mean():.2f}")
    print(f"Recomendação média  : {df['recomendaria'].mean():.2f}")

    resumo = (
        df
        .groupby("area")
        .agg(
            Quantidade       = ("id_funcionario",  "count"),
            Media_Satisfacao = ("nivel_satisfacao", "mean"),
            Media_Indicaria  = ("recomendaria",     "mean")
        )
        .sort_values("Media_Satisfacao")
    )
    print(resumo)
    resumo.to_csv(OUT_RESUMO, encoding="utf-8-sig")
    return resumo


def exportar_dados(df: pd.DataFrame) -> None:
    """Exporta o DataFrame tratado para CSV."""
    df.to_csv(OUT_TRATADA, index=False, encoding="utf-8-sig")
    print(f"Base tratada exportada para: {OUT_TRATADA}")


# ================================================================
# BANCO DE DADOS
# ================================================================

def criar_banco(df: pd.DataFrame, caminho_banco: str) -> None:
    """
    Persiste o DataFrame no banco SQLite e cria Views analíticas.
    Usa context manager para garantir fechamento seguro da conexão.

    Parâmetros:
        df (pd.DataFrame): Dados tratados a serem persistidos.
        caminho_banco (str): Caminho para o arquivo .db do SQLite.
    """
    with sqlite3.connect(caminho_banco) as conn:
        df.to_sql("funcionarios_clima", conn, if_exists="replace", index=False)

        conn.executescript("""
            DROP VIEW IF EXISTS vw_satisfacao_area;
            CREATE VIEW vw_satisfacao_area AS
            SELECT
                area,
                COUNT(*)                        AS total_colaboradores,
                ROUND(AVG(nivel_satisfacao), 2) AS media_satisfacao,
                ROUND(AVG(recomendaria), 2)     AS media_recomendacao
            FROM funcionarios_clima
            GROUP BY area
            ORDER BY media_satisfacao;

            DROP VIEW IF EXISTS vw_cargos;
            CREATE VIEW vw_cargos AS
            SELECT cargo, COUNT(*) AS total
            FROM funcionarios_clima
            GROUP BY cargo;

            DROP VIEW IF EXISTS vw_tempo_empresa;
            CREATE VIEW vw_tempo_empresa AS
            SELECT
                classificacao_experiencia,
                COUNT(*)                        AS total,
                ROUND(AVG(nivel_satisfacao), 2) AS media_satisfacao
            FROM funcionarios_clima
            GROUP BY classificacao_experiencia
            ORDER BY media_satisfacao;
        """)

    print(f"Banco criado com sucesso em: {caminho_banco}")


# ================================================================
# MAIN
# ================================================================

def main() -> None:
    """Orquestra o pipeline completo de clima organizacional."""
    print("Pipeline iniciado.\n")

    try:
        df        = carregar_dados(RAW_CLIMA)
        df_clean  = tratar_dados(df)

        gerar_estatisticas(df_clean)
        resumo_executivo(df_clean)
        exportar_dados(df_clean)
        criar_banco(df_clean, DB_PATH)

        print("\nPipeline concluído com sucesso!")

    except FileNotFoundError as e:
        print(f"\n[ERRO] {e}")
        print("Verifique se o CSV está na pasta correta e tente novamente.")


if __name__ == "__main__":
    main()