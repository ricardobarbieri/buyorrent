import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime
import plotly.express as px

# Configuração da página
st.set_page_config(
    page_title="Simulador de Financiamento vs Aluguel",
    page_icon="🏠",
    layout="wide"
)

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 15px 32px;
        border: none;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Título principal
st.title("💰 Simulador: Comprar ou Alugar?")
st.markdown("---")

# Criando colunas para organizar os inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Dados do Financiamento")
    valor_imovel = st.number_input("Valor do Imóvel (R$)", min_value=0.0, value=300000.0, step=1000.0)
    entrada = st.number_input("Valor da Entrada (R$)", min_value=0.0, value=60000.0, step=1000.0)
    taxa_juros_anual = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, value=8.0, step=0.1)
    prazo_anos = st.number_input("Prazo (anos)", min_value=1, value=30, step=1)

with col2:
    st.subheader("🏠 Dados do Aluguel")
    valor_aluguel = st.number_input("Valor do Aluguel Mensal (R$)", min_value=0.0, value=1500.0, step=100.0)
    reajuste_aluguel_anual = st.number_input("Reajuste Anual do Aluguel (%)", min_value=0.0, value=5.0, step=0.1)
    rendimento_investimento = st.number_input("Rendimento Anual da Entrada se Investida (%)", min_value=0.0, value=6.0, step=0.1)

# Função para calcular prestação do financiamento
def calcular_prestacao(valor, entrada, juros_anual, prazo_anos):
    valor_financiado = valor - entrada
    taxa_mensal = (1 + juros_anual/100)**(1/12) - 1
    n_prestacoes = prazo_anos * 12
    prestacao = valor_financiado * (taxa_mensal * (1 + taxa_mensal)**n_prestacoes) / ((1 + taxa_mensal)**n_prestacoes - 1)
    return prestacao

if st.button("Calcular Simulação"):
    # Cálculos
    prestacao_mensal = calcular_prestacao(valor_imovel, entrada, taxa_juros_anual, prazo_anos)
    
    # Criando arrays para os gráficos
    meses = np.arange(prazo_anos * 12)
    
    # Calculando valores acumulados
    valor_pago_financiamento = np.full(len(meses), prestacao_mensal).cumsum()
    valor_pago_financiamento = valor_pago_financiamento + entrada
    
    # Calculando aluguel com reajuste anual
    aluguel_mensal = np.zeros(len(meses))
    aluguel_atual = valor_aluguel
    for i in range(len(meses)):
        if i % 12 == 0 and i > 0:
            aluguel_atual *= (1 + reajuste_aluguel_anual/100)
        aluguel_mensal[i] = aluguel_atual
    
    valor_pago_aluguel = aluguel_mensal.cumsum()
    
    # Calculando rendimento da entrada se investida
    rendimento_mensal = (1 + rendimento_investimento/100)**(1/12) - 1
    valor_entrada_investida = entrada * (1 + rendimento_mensal)**(meses + 1)
    
    # Criando o gráfico
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=meses/12,
        y=valor_pago_financiamento,
        name='Financiamento (Total Pago)',
        line=dict(color='#FF4B4B', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=meses/12,
        y=valor_pago_aluguel,
        name='Aluguel (Total Pago)',
        line=dict(color='#1F77B4', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=meses/12,
        y=valor_entrada_investida,
        name='Rendimento da Entrada',
        line=dict(color='#2ECC71', width=3)
    ))
    
    fig.update_layout(
        title='Comparação: Financiamento vs Aluguel ao Longo do Tempo',
        xaxis_title='Anos',
        yaxis_title='Valor Total (R$)',
        template='plotly_white',
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Resultados finais
    st.markdown("### 📊 Resultados da Simulação")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Prestação Mensal do Financiamento",
            f"R$ {prestacao_mensal:,.2f}"
        )
    
    with col2:
        st.metric(
            "Total Pago no Financiamento",
            f"R$ {valor_pago_financiamento[-1]:,.2f}"
        )
    
    with col3:
        st.metric(
            "Total Pago em Aluguel",
            f"R$ {valor_pago_aluguel[-1]:,.2f}"
        )
    
    # Análise final
    diferenca = valor_pago_financiamento[-1] - valor_pago_aluguel[-1]
    st.markdown("### 📝 Análise Final")
    if diferenca > 0:
        st.warning(f"Alugar é mais vantajoso financeiramente. Economia de R$ {diferenca:,.2f}")
    else:
        st.success(f"Financiar é mais vantajoso financeiramente. Economia de R$ {abs(diferenca):,.2f}")

# Rodapé
st.markdown("---")
st.markdown("### ℹ️ Considerações Importantes")
st.markdown("""
- Esta simulação é uma simplificação e não considera todos os fatores envolvidos na decisão de comprar ou alugar um imóvel.
- Outros fatores importantes incluem: valorização do imóvel, custos de manutenção, IPTU, condomínio, etc.
- A decisão entre comprar ou alugar também envolve aspectos não financeiros, como estabilidade e preferências pessoais.
""")