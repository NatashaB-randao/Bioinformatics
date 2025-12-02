import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# CONFIGURAÇÃO DA PÁGINA
# =============================================================================
st.set_page_config(page_title="Dashboard Soja", layout="wide")

st.title("🌽 Dashboard Estratégico: Soja & Câmbio")
st.markdown("Análise de sazonalidade, correlação cambial e inteligência de mercado.")

# =============================================================================
# CARREGAMENTO DE DADOS
# =============================================================================
@st.cache_data # Isso faz o app ficar rápido (não recarrega o CSV toda hora)
def carregar_dados():
    # Lê o arquivo que você baixou do Kaggle
    df = pd.read_csv("soja_dashboard_final.csv")
    df['data'] = pd.to_datetime(df['data'])
    df['Ano'] = df['data'].dt.year
    return df

try:
    df = carregar_dados()
except FileNotFoundError:
    st.error("Erro: O arquivo 'soja_dashboard_final.csv' não foi encontrado na pasta.")
    st.stop()

# =============================================================================
# BARRA LATERAL (FILTROS)
# =============================================================================
st.sidebar.header("Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df['Ano'].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione os Anos:", 
    anos_disponiveis, 
    default=anos_disponiveis[-4:] # Padrão: Últimos 4 anos
)

# Aplicando filtro
if anos_selecionados:
    df_filtrado = df[df['Ano'].isin(anos_selecionados)]
else:
    df_filtrado = df # Se não selecionar nada, mostra tudo

# =============================================================================
# KPIS (INDICADORES DE TOPO)
# =============================================================================
ultimo_dado = df.iloc[-1]
var_mes = ultimo_dado['var_soja_pct']

col1, col2, col3 = st.columns(3)
col1.metric("Preço da Soja (Saca)", f"R$ {ultimo_dado['preco_soja_brl']:.2f}", f"{var_mes:.2f}%")
col2.metric("Dólar PTAX", f"R$ {ultimo_dado['dolar_ptax']:.4f}", f"{ultimo_dado['var_dolar_pct']:.2f}%")
col3.metric("Fase da Safra Atual", ultimo_dado['status_safra'])

st.divider()

# =============================================================================
# GRÁFICOS INTERATIVOS
# =============================================================================

# --- GRÁFICO 1: EVOLUÇÃO TEMPORAL (EIXO DUPLO) ---
fig_evolucao = make_subplots(specs=[[{"secondary_y": True}]])

# Linha Soja
fig_evolucao.add_trace(
    go.Scatter(x=df_filtrado['data'], y=df_filtrado['preco_soja_brl'], name="Preço Soja",
               line=dict(color='#1f77b4', width=2)), secondary_y=False
)

# Linha Dólar
fig_evolucao.add_trace(
    go.Scatter(x=df_filtrado['data'], y=df_filtrado['dolar_ptax'], name="Dólar",
               line=dict(color='#ff7f0e', width=2, dash='dot')), secondary_y=True
)

fig_evolucao.update_layout(title="<b>Evolução Diária: Preço vs. Câmbio</b>", height=500, hovermode="x unified")
fig_evolucao.update_yaxes(title_text="Preço Soja (R$)", secondary_y=False)
fig_evolucao.update_yaxes(title_text="Dólar", secondary_y=True, showgrid=False)

st.plotly_chart(fig_evolucao, use_container_width=True)

# --- LINHA 2: DOIS GRÁFICOS LADO A LADO ---
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    st.subheader("Sazonalidade (Heatmap)")
    # Pivotando para o Heatmap
    heatmap_data = df.pivot_table(values='preco_soja_brl', index='Ano', columns='mes', aggfunc='mean')
    
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='RdYlGn'
    ))
    fig_heat.update_layout(height=400, title="Preço Médio por Mês/Ano")
    st.plotly_chart(fig_heat, use_container_width=True)

with col_graf2:
    st.subheader("Dispersão (Correlação)")
    fig_scat = go.Figure(data=go.Scatter(
        x=df_filtrado['dolar_ptax'],
        y=df_filtrado['preco_soja_brl'],
        mode='markers',
        marker=dict(color='steelblue', opacity=0.6)
    ))
    fig_scat.update_layout(
        height=400, title="Dólar vs Soja",
        xaxis_title="Dólar", yaxis_title="Soja (R$)"
    )
    st.plotly_chart(fig_scat, use_container_width=True)

# =============================================================================
# RELATÓRIO EXECUTIVO (Final)
# =============================================================================
st.divider()
st.subheader("📑 Relatório Executivo")
st.markdown("""
- **Sazonalidade Confirmada:** Identificamos queda média de preços nos meses de **Março e Abril** (Safra).
- **Correlação:** O ativo apresenta forte correlação positiva com o dólar, exigindo proteção cambial.
- **Recomendação:** Evitar venda spot no primeiro trimestre.
""")