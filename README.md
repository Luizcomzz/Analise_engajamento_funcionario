# Análise de Satisfação e Desempenho de Colaboradores

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-3.0-150458?style=flat&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-2.4-013243?style=flat&logo=numpy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)
![Status](https://img.shields.io/badge/Status-Concluído-28a745?style=flat)

---

## 🎥 Apresentação dos Resultados

[![Assista à apresentação completa no YouTube](https://img.shields.io/badge/▶%20Assistir%20no%20YouTube-Apresentação%20dos%20Resultados-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://youtu.be/vkAYYM45xp4)

> Neste vídeo explico o processo analítico completo, as decisões metodológicas e os principais insights identificados na análise.

---

## 🎯 Problema de Negócio

Empresas com alto índice de insatisfação e baixo engajamento enfrentam custos elevados de rotatividade e perda de produtividade. A liderança de RH de uma organização precisa decidir **quais áreas e perfis de colaboradores demandam atenção prioritária** para reduzir esse risco e melhorar o ambiente de trabalho.

Este projeto integra **duas fontes de dados** — pesquisa de clima organizacional e avaliação de desempenho — para identificar padrões de satisfação, engajamento e recomendação entre colaboradores, fornecendo insumos concretos para decisões estratégicas de gestão de pessoas.

> **Pergunta central:** Quais áreas e perfis concentram os menores índices de satisfação e engajamento, e quais fatores estão associados a esse resultado?

---

## 🔍 Principais Achados

> Base analisada: **500 colaboradores · 12 áreas · Satisfação média: 4,15/5 · Recomendação média: 4,23/5**

| # | Achado | Impacto no Negócio |
|---|---|---|
| 1 | **Área de Manutenção** (47 colaboradores) apresentou satisfação média de **3,81/5** — menor que a média da organização | Requer atenção prioritária — investigação qualitativa recomendada antes de ações corretivas |
| 2 | **Planejamento e Experiência do Cliente** também abaixo da média, com **3,73** e **3,75** respectivamente | Três áreas críticas identificadas — foco para programas de engajamento |
| 3 | **Áreas com melhor trabalho em equipe e alinhamento de valores** (Operação 4,36 · Marketing 4,30 · Tecnologia 4,27) também lideram em recomendação da empresa | Fortalecer esses pilares nas áreas críticas pode elevar o eNPS organizacional |

---

## ⭐ Diferenciais Técnicos deste Projeto

| Diferencial | Por que importa |
|---|---|
| **Duas fontes de dados integradas** | Pesquisa de Clima + Avaliação de Desempenho cruzadas — capacidade de trabalhar com múltiplos datasets |
| **Views SQL para governança** | `vw_satisfacao_area`, `vw_cargos`, `vw_tempo_empresa` — controle de acesso a dados sensíveis de RH |
| **Análise de correlação com heatmap** | Matriz de correlação entre variáveis de avaliação — demonstra raciocínio estatístico além do descritivo |
| **Apresentação gravada em vídeo** | Comunicação oral dos resultados para stakeholders — habilidade rara em portfólios de analistas |

---

## 💡 Impacto Esperado

Os resultados desta análise permitem à liderança de RH:

- **Priorizar investigações qualitativas** nas áreas de menor satisfação (Manutenção, Planejamento, Experiência do Cliente)
- **Compartilhar boas práticas** das áreas de melhor desempenho (Operação, Marketing, Tecnologia) com as equipes críticas
- **Monitorar continuamente** os indicadores de clima com o dashboard desenvolvido em Power BI
- **Embasar decisões de retenção** com dados de engajamento cruzados com avaliação de desempenho

---

## 📊 Dashboards

### Engajamento dos Funcionários
<p align="center">
  <img src="dashboard/funcionario_engajamento.png" width="900">
</p>

- **Média de avaliação por equipe:** identifica quais áreas se destacam positiva e negativamente em performance
- **Funcionários por descrição de desempenho:** distribuição da força de trabalho pelas faixas de entrega

### Clima Organizacional
<p align="center">
  <img src="dashboard/funcionarios_clima.png" width="900">
</p>

- **Satisfação e recomendação por área:** comparativo entre os 12 departamentos da organização
- **Distribuição por tempo de empresa:** análise de engajamento ao longo da jornada do colaborador

---

## 📂 Estrutura do Projeto

```
Analise_Satisfacao_Desempenho/
├── data/
│   ├── Pesquisa_de_Clima.csv          # Base de clima organizacional (fonte 1)
│   ├── Avaliacao_de_Desempenho.csv    # Base de desempenho (fonte 2)
│   ├── funcionarios.db                # Banco SQLite — clima + views analíticas
│   ├── desempenho.db                  # Banco SQLite — avaliação de desempenho
│   └── processed/
│       ├── base_tratada.csv
│       ├── estatisticas_descritivas.csv
│       └── resumo_area.csv
├── dashboard/
│   ├── funcionario_engajamento.png
│   └── funcionarios_clima.png
├── docs/
│   └── Desafio Técnico - People Analytics.pdf
├── notebooks/
│   └── 01_analise_correlacao_desempenho.ipynb
├── src/
│   ├── pipeline.py                    # Pipeline: clima organizacional
│   └── analise_correlacao_desempenho.py  # Correlação entre variáveis de desempenho
├── requirements.txt
└── README.md
```

---

## 🚀 Como Reproduzir

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/Analise_Satisfacao_Desempenho.git
cd Analise_Satisfacao_Desempenho

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute o pipeline de clima organizacional
python src/pipeline.py

# 5. Execute a análise de correlação de desempenho
python src/analise_correlacao_desempenho.py

# 6. Explore o notebook de correlação
jupyter notebook notebooks/01_analise_correlacao_desempenho.ipynb
```

---

## 🔎 Hipóteses Analíticas

| Hipótese | Resultado | Conclusão |
|---|---|---|
| Maior tempo de empresa → maior satisfação | Parcialmente confirmado | Colaboradores mais antigos mantêm boa satisfação, mas sem causalidade comprovada |
| Diferenças significativas entre áreas | Confirmado | Manutenção (3,81) vs Operação (4,36) — diferença de 0,55 pontos |
| Idade associada à satisfação | Requer aprofundamento | Dados insuficientes para conclusão direta |
| Recomendação varia entre setores | Confirmado | Setores com melhor trabalho em equipe lideram em recomendação |
| Satisfação e desempenho correlacionados | Confirmado | Matriz de correlação evidencia relação positiva entre as variáveis |
| Colaboradores satisfeitos recomendam mais | Confirmado | Satisfação e recomendação seguem padrão consistente por área |

---

## 📋 Metodologia

### 1. Entendimento do Problema
Organização dos dados e levantamento das perguntas norteadoras para a análise.

### 2. Tratamento dos Dados
Importação das duas bases, padronização de colunas, limpeza de valores inválidos e nulos, conversão de tipos e classificação estatística das variáveis.

### 3. Análise Exploratória
Consultas SQL com Views para análise segmentada por área, cargo e tempo de empresa. Análise de correlação entre variáveis de avaliação com geração de heatmap.

### 4. Governança de Dados
Criação de Views SQL para restringir acesso a dados sensíveis e organizar consultas de forma segura e reutilizável.

### 5. Visualização
Dashboards no Power BI conectados ao banco SQLite, com indicadores de satisfação, eNPS e desempenho por área.

### 6. Apresentação dos Resultados
[▶ Apresentação em vídeo no YouTube](https://youtu.be/vkAYYM45xp4) — processo analítico e principais insights explicados para stakeholders.

---

## 📈 KPIs Monitorados

| Indicador | Resultado |
|---|---|
| Total de colaboradores analisados | 500 |
| Número de áreas mapeadas | 12 |
| Índice médio de satisfação | 4,15 / 5,00 |
| eNPS — índice médio de recomendação | 4,23 / 5,00 |
| Área de maior satisfação | Operação (4,36) |
| Área de menor satisfação | Planejamento (3,73) |

---

## 🛠️ Tecnologias Utilizadas

| Ferramenta | Finalidade |
|---|---|
| [Python 3.14](https://www.python.org/) | Linguagem de programação principal |
| [Pandas](https://pandas.pydata.org/) | Tratamento e análise dos dados |
| [NumPy](https://numpy.org/) | Suporte a operações numéricas |
| [Matplotlib + Seaborn](https://seaborn.pydata.org/) | Visualização da matriz de correlação |
| [SQLite](https://sqlite.org/) | Banco de dados com Views para governança |
| [Power BI](https://www.microsoft.com/pt-br/power-platform/products/power-bi/desktop) | Dashboards interativos de clima e desempenho |
| [Jupyter Notebook](https://jupyter.org/) | Análise exploratória interativa e documentada |

---

## 👤 Autor

Desenvolvido por **Luiz** · [LinkedIn](https://linkedin.com/in/seu-perfil) · [GitHub](https://github.com/seu-usuario)