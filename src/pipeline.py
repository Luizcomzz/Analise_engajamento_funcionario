import pandas as pd 
import numpy as np
import sqlite3 as sql 

# Com esse script só preciso criar uma vez e posso rodar o arquivo csv que desejar 
def carregar_dados(caminho):
    # Verifica a extensão do arquivo para aplicar a função correta
    if caminho.endswith('.csv'):
        return pd.read_csv(caminho, header=0, encoding="utf-8")
    else:
        # Removido o parâmetro encoding que causava erro no Excel
        return pd.read_excel(caminho, header=0)
    
    print("Seus dados foram importados")

df = carregar_dados('data/Pesquisa_de_Clima.csv')
df.info()

"""Mostras as medidas estatisticas de cada coluna
Como Contagem, média, max, min, desvio padrao e quartils
"""

print("\n=== ESTATÍSTICAS DESCRITIVAS ===")
print(df.describe(include="all").T) #Esse.t é a matriz transposta, que as vezes facilita a leitura 

#Mostra as 5 primeiras linhas de dados
print( f"\n=== Primeiras linhas da tabela ===\n {df.head()}")

def tratar_dados(df):

    df = df.copy()

    df.columns = df.columns.str.lower().str.strip()

    df = df.rename(columns={
        'aval_valores': 'avaliacao_valores',
        'aval_performace': 'avaliacao_performance',
        'aval_equipe': 'avaliacao_equipe',
        'desc_satisfacao': 'descricao_satisfacao',
        'desc_recomendaria': 'descricao_recomendaria',
        'class_experiencia': 'classificacao_experiencia'
    })

    return df

    # Classificação Estatistica de variáveis
#Separa cada coluna em tipos de variáveis
qualitativas_ordinais =  (['avaliacao_valores','avaliacao_performace', 'avaliacao_equipe', 'faixa_idade','descricao_satisfacao','descricao_recomendaria'])

qualitativas_nominais = ['apelido', 'area', 'cargo']

quantitativas_discretas = ['id_funcionario', 'idade', 'nivel_satisfacao', 'recomendaria']

quantitativas_continuas = ['anos_na_empresa', 'classificacao_experiencia']

classificacao_estatistica = {
    **{coluna: "Qualitativa ordinal"
       for coluna in qualitativas_ordinais},

    **{coluna: "Qualitativa nominal"
       for coluna in qualitativas_nominais},

    **{coluna: "Quantitativa discreta"
       for coluna in quantitativas_discretas},

    **{coluna: "Quantitativa contínua"
       for coluna in quantitativas_continuas}
}
df = tratar_dados(df)
print(df.columns)

tabela_variaveis = pd.DataFrame({
    "variavel": df.columns,
    "tipo_inicial_pandas": [
        str(df[coluna].dtype)
        for coluna in df.columns
    ],
    "classificacao_estatistica": [
        classificacao_estatistica[coluna]
        for coluna in df.columns

    ],
    "quantidade_valores_distintos": [
        df[coluna].nunique(dropna=True)
        for coluna in df.columns
    ],
    "exemplos_de_valores": [
        df[coluna]
        .dropna()
        .drop_duplicates()
        .head(3)
        .tolist()
        for coluna in df.columns
    ]
})



print(tabela_variaveis)



