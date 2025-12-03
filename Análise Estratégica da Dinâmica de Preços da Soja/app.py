import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =============================================================================
# 1. CONFIGURAÇÃO VISUAL (LAYOUT PROFISSIONAL)
# =============================================================================
st.set_page_config(
    page_title="Intelligence Desk | Soja",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Customizado para ajustar espaçamentos e fontes (Visual Clean)
st.markdown("""
<style>
    .block-container {padding-top: 1.5rem; padding-bottom: 3rem;}
    [data-testid="stMetricValue"] {font-size: 1.7rem !important;}
</style>
""", unsafe_allow_html=True)

# =============================================================================
# 2. CARGA DE DADOS
# =============================================================================
@st.cache_data
def carregar_dados():
    try:
        # Carrega o CSV que você salvou no Kaggle
        df = pd.read_csv("soja_dashboard_final.csv")
        df['data'] = pd.to_datetime(df['data'])
        df['Ano'] = df['data'].dt.year
        df['Mes'] = df['data'].dt.month
        return df.sort_values('data')
    except FileNotFoundError:
        st.error("⚠️ Erro Crítico: O arquivo 'soja_dashboard_final.csv' não foi encontrado na pasta.")
        st.stop()

df_raw = carregar_dados()

# =============================================================================
# 3. SIDEBAR (FILTROS AVANÇADOS)
# =============================================================================
with st.sidebar:
    st.header("🎛️ Filtros de Análise")
    st.markdown("---")
    
    # 1. Filtro de Data
    min_date = df_raw['data'].min().date()
    max_date = df_raw['data'].max().date()
    
    datas = st.date_input(
        "Período de Análise:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Validação de data
    if len(datas) == 2:
        start_date, end_date = datas
    else:
        start_date, end_date = min_date, max_date

    st.markdown("---")

    # 2. Filtro de Fase da Safra (MULTISELEÇÃO - O que você pediu!)
    fases_disponiveis = sorted(df_raw['status_safra'].unique())
    fases_selecionadas = st.multiselect(
        "Fases do Ciclo:",
        options=fases_disponiveis,
        default=fases_disponiveis, # Vem tudo marcado por padrão
        placeholder="Selecione fases para comparar..."
    )
    
    # 3. Filtro de Anos (MULTISELEÇÃO)
    anos_disponiveis = sorted(df_raw['Ano'].unique())
    anos_selecionados = st.multiselect(
        "Anos Fiscais:",
        options=anos_disponiveis,
        default=anos_disponiveis
    )

# --- MOTOR DE FILTRAGEM (CRUZAMENTO DE FILTROS) ---
mask = (
    (df_raw['data'].dt.date >= start_date) & 
    (df_raw['data'].dt.date <= end_date) &
    (df_raw['status_safra'].isin(fases_selecionadas)) &
    (df_raw['Ano'].isin(anos_selecionados))
)
df_filtered = df_raw.loc[mask]

# Tratamento de erro se o filtro zerar os dados
if df_filtered.empty:
    st.warning("⚠️ Nenhum dado encontrado com essa combinação de filtros. Tente selecionar mais fases ou anos.")
    st.stop()

# =============================================================================
# 4. DASHBOARD EXECUTIVO (KPIs DINÂMICOS)
# =============================================================================
st.title("🌽 Intelligence Desk: Dinâmica de Mercado")
st.markdown(f"**Status:** {len(df_filtered)} registros filtrados • **Período:** {start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}")

# Pega o último dado DO FILTRO (Dinâmico)
ultimo = df_filtered.iloc[-1]
# Tenta pegar o penúltimo para calcular variação, se não existir, usa o mesmo
penultimo = df_filtered.iloc[-2] if len(df_filtered) > 1 else ultimo

col1, col2, col3, col4 = st.columns(4)

with col1:
    delta_val = ultimo['preco_soja_brl'] - penultimo['preco_soja_brl']
    st.metric(
        "Preço Soja (Saca)", 
        f"R$ {ultimo['preco_soja_brl']:.2f}", 
        f"{delta_val:.2f} R$", 
        delta_color="normal"
    )

with col2:
    delta_dol = ultimo['dolar_ptax'] - penultimo['dolar_ptax']
    st.metric(
        "Dólar PTAX", 
        f"R$ {ultimo['dolar_ptax']:.4f}", 
        f"{delta_dol:.4f} R$", 
        delta_color="inverse" # Para dólar, subida fica vermelha (custo)
    )

with col3:
    # Média do período selecionado
    media_periodo = df_filtered['preco_soja_brl'].mean()
    st.metric(
        "Preço Médio (Filtro)", 
        f"R$ {media_periodo:.2f}",
        help="Média de preço considerando apenas os dias filtrados."
    )

with col4:
    # Mostra a fase atual do último dia filtrado
    safra_atual = ultimo['status_safra'].split(".")[1] if "." in ultimo['status_safra'] else ultimo['status_safra']
    st.metric("Fase do Ciclo (Atual)", safra_atual)

st.divider()

# =============================================================================
# 5. ÁREA DE ANÁLISE (ABAS)
# =============================================================================
tab1, tab2, tab3 = st.tabs(["📈 Visão de Mercado", "🧠 Análise Sazonal (Boxplot)", "📋 Dados Analíticos"])

# --- ABA 1: GRÁFICO TEMPORAL ---
with tab1:
    st.subheader("Evolução Temporal: Soja vs. Dólar")
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Soja (Área)
    fig.add_trace(go.Scatter(
        x=df_filtered['data'], y=df_filtered['preco_soja_brl'], name="Preço Soja",
        line=dict(color='#00D4FF', width=3), fill='tozeroy', fillcolor='rgba(0, 212, 255, 0.1)'
    ), secondary_y=False)
    
    # Dólar (Linha)
    fig.add_trace(go.Scatter(
        x=df_filtered['data'], y=df_filtered['dolar_ptax'], name="Dólar",
        line=dict(color='#FF4B4B', width=2, dash='dot')
    ), secondary_y=True)

    fig.update_layout(
        height=500, 
        template="plotly_dark", 
        hovermode="x unified",
        margin=dict(l=0, r=0, t=50, b=0),
        legend=dict(orientation="h", y=1.1)
    )
    st.plotly_chart(fig, use_container_width=True)

# --- ABA 2: BOXPLOT INTERATIVO (CORRIGIDO) ---
with tab2:
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Dispersão de Preços por Fase da Safra")
        st.caption("Compare a volatilidade de preços entre as fases selecionadas no menu lateral.")
        
        # O SEGREDO: Usar px.box com df_filtered. 
        # Isso cria o gráfico interativo que funciona no dark mode.
        fig_box = px.box(
            df_filtered, 
            x="status_safra", 
            y="preco_soja_brl", 
            color="status_safra",
            points="outliers", # Mostra outliers
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig_box.update_layout(
            height=500, 
            template="plotly_dark", 
            showlegend=False,
            xaxis_title=None,
            yaxis_title="Preço (R$)"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    with col_right:
        st.subheader("Correlação (Scatter)")
        st.caption("Relação Dólar x Preço no período filtrado.")
        
        # Scatter Plot dinâmico
        corr_val = df_filtered['preco_soja_brl'].corr(df_filtered['dolar_ptax'])
        
        fig_scat = px.scatter(
            df_filtered, x="dolar_ptax", y="preco_soja_brl",
            trendline="ols", trendline_color_override="red",
            title=f"Pearson: {corr_val:.2f}"
        )
        fig_scat.update_layout(height=500, template="plotly_dark", margin=dict(t=50))
        st.plotly_chart(fig_scat, use_container_width=True)

# --- ABA 3: DADOS ---
with tab3:
    st.subheader("Base de Dados Filtrada")
    st.markdown("Visualize os dados brutos resultantes dos filtros aplicados.")
    
    # Dataframe Interativo do Streamlit
    st.dataframe(
        df_filtered,
        use_container_width=True,
        height=500,
        column_order=["data", "preco_soja_brl", "dolar_ptax", "status_safra", "var_soja_pct"],
        column_config={
            "data": st.column_config.DateColumn("Data", format="DD/MM/YYYY"),
            "preco_soja_brl": st.column_config.NumberColumn("Preço Soja", format="R$ %.2f"),
            "dolar_ptax": st.column_config.NumberColumn("Dólar", format="R$ %.4f"),
            "var_soja_pct": st.column_config.NumberColumn("Var %", format="%.2f %%"),
        }
    )