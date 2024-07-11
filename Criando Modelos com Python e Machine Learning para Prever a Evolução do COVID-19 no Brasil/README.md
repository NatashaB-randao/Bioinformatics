# Previsão de Casos Confirmados de COVID-19 no Brasil

Este projeto tem como objetivo prever o crescimento dos casos confirmados de COVID-19 no Brasil utilizando dados de um desafio do Kaggle do ano de 2020.

## Sumário

- [Introdução](#introdução)
- [Instalação](#instalação)
- [Descrição dos Dados](#descrição-dos-dados)
- [Pré-processamento](#pré-processamento)
- [Análise Exploratória](#análise-exploratória)
- [Modelagem](#modelagem)
- [Visualização](#visualização)
- [Conclusão](#conclusão)
- [Referências](#referências)

## Introdução

Com a pandemia de COVID-19, houve a necessidade de desenvolver modelos preditivos que pudessem auxiliar na compreensão da evolução da doença e na tomada de decisões. Este projeto utiliza a biblioteca Prophet, desenvolvida pelo Facebook, para modelar e prever os casos confirmados de COVID-19 no Brasil.

## Instalação

Para executar este projeto, é necessário ter o Python instalado e as seguintes bibliotecas:

```bash
pip install pandas numpy matplotlib seaborn plotly prophet
```

Caso esteja utilizando Jupyter Notebook, certifique-se de que as bibliotecas `jupyter` e `ipywidgets` estão atualizadas:

```bash
pip install --upgrade jupyter ipywidgets
```

## Descrição dos Dados

Os dados utilizados neste projeto são provenientes de um desafio do Kaggle de 2020 e contêm informações diárias sobre os casos confirmados de COVID-19 no Brasil.

## Pré-processamento

No pré-processamento, os dados foram renomeados e ajustados para serem utilizados no modelo Prophet. A coluna de datas foi renomeada para `ds` e a coluna de casos confirmados para `y`. A população brasileira foi utilizada como um limite superior (`cap`) para o crescimento dos casos.

```python
# Renomeando Colunas
train.rename(columns={'observationdate': 'ds', 'confirmed': 'y'}, inplace=True)
test.rename(columns={'observationdate': 'ds', 'confirmed': 'y'}, inplace=True)

# Definindo a capacidade de crescimento
pop = 211463156
train['cap'] = pop
```

## Análise Exploratória

A análise exploratória dos dados foi realizada utilizando gráficos interativos para melhor compreensão da evolução dos casos confirmados, mortes, sazonalidade e tendência.

```python
# Exemplos de gráficos interativos
fig = go.Figure()
fig.add_trace(go.Scatter(x=brasil.observationdate, y=brasil.confirmed, name='Casos Confirmados', mode='lines'))
fig.update_layout(title='Casos Confirmados de COVID-19 no Brasil')
fig.show()
```

## Modelagem

Para a modelagem, utilizamos o algoritmo ARIMA para análise de séries temporais e o Prophet para prever o crescimento dos casos confirmados.

### ARIMA

O ARIMA (Autoregressive Integrated Moving Average) é um método utilizado para modelar e prever séries temporais. Este método considera a autocorrelação entre os dados e realiza a diferenciação para tornar a série estacionária.

```markdown
**Modelo ARIMA**
O modelo ARIMA é utilizado para analisar e prever séries temporais. Ele considera a autocorrelação dos dados e realiza diferenciação para estabilizar a série. A sigla ARIMA significa Autoregressive Integrated Moving Average (Modelo Autorregressivo Integrado de Médias Móveis).
```

### Prophet

O Prophet é uma ferramenta desenvolvida pelo Facebook para previsões de séries temporais que apresentam sazonalidade e tendência de crescimento. Ele permite a inclusão de pontos de mudança na tendência e capacidade de crescimento logístico.

```python
# Definir o Modelo de Crescimento
profeta = Prophet(growth='logistic', changepoints=['2020-03-21', '2020-03-30', '2020-04-25', '2020-05-03', '2020-05-10'])
profeta.fit(train)

# Construit Previsões para o Futuro
future_dates = profeta.make_future_dataframe(periods=200)
future_dates['cap'] = pop
forecast = profeta.predict(future_dates)
```

## Visualização

As previsões foram visualizadas utilizando a biblioteca Plotly para gráficos interativos. O gráfico apresenta os valores observados, preditos e a previsão para os próximos 30 dias.

```python
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=confirmados.index, y=confirmados, name='Observados', mode='markers', marker=dict(color='red')
))

fig.add_trace(go.Scatter(
    x=confirmados.index, y=modelo.predict_in_sample(), name='Preditos'
))

fig.add_trace(go.Scatter(
    x=pd.date_range('2020-05-20', '2020-06-20'), y=modelo.predict(31), name='Forecast'
))

fig.update_layout(title='Previsão de Casos Confirmados no Brasil para os Próximos 30 Dias')

fig.show()
```

## Conclusão

Este projeto demonstrou a aplicação de técnicas de modelagem de séries temporais para prever o crescimento dos casos confirmados de COVID-19 no Brasil. Utilizando os modelos ARIMA e Prophet, foi possível criar previsões que podem auxiliar na tomada de decisões durante a pandemia.

## Referências

- [Prophet Documentation](https://facebook.github.io/prophet/)
- [Kaggle COVID-19 Challenge](https://www.kaggle.com/c/covid19-global-forecasting)
- [Statsmodels Documentation](https://www.statsmodels.org/)
- [Plotly Documentation](https://plotly.com/python/)

