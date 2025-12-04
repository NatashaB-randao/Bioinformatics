# 🌱 Análise Estratégica: Dinâmica de Preços da Soja (2018-2025)

![Python](https://img.shields.io/badge/Python-3.11%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)
![Status](https://img.shields.io/badge/Status-Concluído-success)

> **Intelligence Desk:** Um projeto de Data Analytics end-to-end focado em desvendar padrões de sazonalidade, correlação cambial e janelas de arbitragem no agronegócio brasileiro.

---

## 💼 O Problema de Negócio
O agronegócio brasileiro é altamente dependente de fatores externos. Produtores rurais, tradings e indústrias enfrentam diariamente o dilema da comercialização: **"Vender agora ou segurar o produto?"**.

Decisões baseadas apenas no *feeling* geram prejuízos milionários devido à alta volatilidade do mercado. Este projeto visa responder, com dados, às seguintes perguntas estratégicas:
1.  Existe um padrão estatístico confiável de queda de preços na colheita?
2.  Qual é a real correlação entre o Dólar e a Soja? O ativo é 100% dolarizado?
3.  Qual o prêmio histórico de risco ao carregar a soja da safra até a entressafra?

---

## 🛠️ A Solução (Pipeline de Dados)
O projeto seguiu a metodologia **CRISP-DM**, estruturado nas seguintes etapas:

1.  **Engenharia de Dados (ETL):**
    * Coleta automatizada de dados macroeconômicos (Yahoo Finance API).
    * Tratamento de dados físicos (CEPEA/Esalq) com limpeza de arquivos "sujos" e unificação de bases temporais.
2.  **Engenharia de Atributos:**
    * Criação de flags de **Ciclo Agrícola** (Plantio, Desenvolvimento, Colheita, Entressafra).
    * Cálculo de Médias Móveis e Volatilidade (Rolling Std).
3.  **Análise Exploratória (EDA):**
    * Decomposição de Séries Temporais (Trend, Seasonal, Residual).
    * Análise de Correlação de Pearson e Regressão Linear.
4.  **Produto Final:**
    * Desenvolvimento de um **Dashboard Interativo em Streamlit** para monitoramento de KPIs.

---

## 📊 Principais Insights (Key Findings)

Com base na análise de **1.882 dias de negociação** (2018-2025), descobrimos:

### 1. A Janela de Arbitragem (Sazonalidade)
A "Lei da Oferta e Procura" atua fortemente no mercado físico.
* 📉 **Compra:** Historicamente, os meses de **Março e Abril (Colheita)** apresentam as medianas de preço mais baixas, devido ao Choque de Oferta.
* 📈 **Venda:** O preço tende a recuperar-se no segundo semestre, atingindo o pico durante o **Plantio (Out-Dez)**.
* **Resultado:** A retenção estratégica gerou, em média, uma valorização bruta de **~8,2%** entre a colheita e o plantio.

### 2. A Tese da Dolarização
* A correlação entre USD/BRL e Soja é **Forte e Positiva (Pearson: ~0.70)**.
* **Alerta:** Em patamares de preço muito altos, ocorre um "descolamento", onde choques de oferta (quebras de safra) superam a influência do câmbio.

### 3. Risco e Volatilidade
* A Soja apresentou uma volatilidade (CV%) de **29,4%**, quase o dobro da volatilidade do Dólar (14,8%). Isso reforça a necessidade de operações de *Hedge*.

---

## 🖥️ O Dashboard (Streamlit)

Foi desenvolvido um painel interativo **Dark Mode** para tomada de decisão, contendo:
* **KPIs Dinâmicos:** Monitoramento de preço spot, variação diária e status da safra.
* **Filtros Cruzados:** Seleção múltipla por Fase da Safra e Ano Fiscal.
* **Visualização Avançada:** Gráficos Plotly interativos (Zoom, Tooltip) substituindo visuais estáticos.

### Previsão Visual:
*(Insira aqui um GIF ou Print do seu Dashboard rodando)*

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
* Python 3.10 ou superior.

### Instalação
1.  Clone o repositório:
    ```bash
    git clone [https://github.com/seu-usuario/analise-soja.git](https://github.com/seu-usuario/analise-soja.git)
    cd analise-soja
    ```

2.  Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

3.  Execute o Dashboard:
    ```bash
    streamlit run app.py
    ```

---

## 🧰 Tecnologias Utilizadas
* **Linguagem:** Python 
* **Análise de Dados:** Pandas, NumPy, Statsmodels.
* **Visualização:** Plotly (Graph Objects & Express), Seaborn, Matplotlib.
* **Web App:** Streamlit.
* **Fonte de Dados:** CEPEA (Esalq/USP) e Banco Central do Brasil.

---

## 📞 Contato
**Autor:** Natasha Brandão
* [LinkedIn](https://www.linkedin.com/in/natasha-brand%C3%A3o/)
* [Portfólio](https://natashab-randao.github.io/Natasha-Brandao-Data-Analyst/)

---
*Disclaimer: Este projeto tem fins estritamente educacionais e analíticos, não configurando recomendação de investimento.*