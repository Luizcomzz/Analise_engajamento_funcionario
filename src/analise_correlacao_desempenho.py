import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ================================================================
# Constantes
# ================================================================
RAW_DESEMPENHO = "data/Avaliacao_de_Desempenho.csv"
DB_DESEMPENHO  = "data/desempenho.db"

VARIAVEIS_NUMERICAS = [
    "Aval_Valores",
    "Aval_Performace",
    "Aval_Equipe"
]


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
# BANCO DE DADOS
# ================================================================

def criar_banco(df: pd.DataFrame, caminho_banco: str) -> None:
    """
    Persiste o DataFrame na tabela 'funcionarios' do banco SQLite.
    Usa context manager para garantir fechamento seguro da conexão.

    Parâmetros:
        df (pd.DataFrame): Dados a serem persistidos.
        caminho_banco (str): Caminho para o arquivo .db.
    """
    with sqlite3.connect(caminho_banco) as conn:
        df.to_sql("funcionarios", conn, if_exists="replace", index=False)

    print(f"Banco criado com sucesso em: {caminho_banco}")


# ================================================================
# ANÁLISE DE CORRELAÇÃO
# ================================================================

def calcular_correlacao(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a matriz de correlação entre as variáveis de avaliação.

    Parâmetros:
        df (pd.DataFrame): DataFrame com as colunas de avaliação.

    Retorna:
        pd.DataFrame: Matriz de correlação.
    """
    colunas_ausentes = [c for c in VARIAVEIS_NUMERICAS if c not in df.columns]
    if colunas_ausentes:
        raise ValueError(f"Colunas não encontradas no DataFrame: {colunas_ausentes}")

    return df[VARIAVEIS_NUMERICAS].corr()


def exibir_heatmap(matriz_correlacao: pd.DataFrame) -> None:
    """
    Exibe um heatmap da matriz de correlação usando Seaborn.

    Parâmetros:
        matriz_correlacao (pd.DataFrame): Matriz de correlação a ser visualizada.
    """
    plt.figure(figsize=(10, 7))

    sns.heatmap(
        matriz_correlacao,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        linewidths=0.5
    )

    plt.title("Matriz de Correlação — Avaliação de Desempenho", fontsize=14)
    plt.tight_layout()
    plt.show()


# ================================================================
# MAIN
# ================================================================

def main() -> None:
    """Orquestra a análise de correlação dos dados de desempenho."""
    print("Análise de correlação iniciada.\n")

    try:
        df     = carregar_dados(RAW_DESEMPENHO)
        criar_banco(df, DB_DESEMPENHO)

        matriz = calcular_correlacao(df)
        print("\n--- Matriz de Correlação ---")
        print(matriz)

        exibir_heatmap(matriz)

        print("\nAnálise concluída com sucesso!")

    except (FileNotFoundError, ValueError) as e:
        print(f"\n[ERRO] {e}")


if __name__ == "__main__":
    main()