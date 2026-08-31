import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Cat Piercer - Precificação",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Estilo visual moderno e escuro (combinando com o estúdio)
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .metric-card {
        background-color: #1a1c23;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #30323d;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💎 Cat Piercer - Simulador de Preço")
st.markdown("Calculadora automática e precisa de custos e margem de lucro por procedimento.")

with st.expander("⚙️ Parâmetros Fixos do Estúdio (Setembro)"):
    salario = st.number_input("Salário Desejado (Pró-labore)", value=2500.0)
    aluguel = st.number_input("Aluguel + Energia + Água", value=650.0)
    transporte = st.number_input("Transporte Mensal", value=288.0)
    dias = st.number_input("Dias Trabalhados no Mês", value=12)
    horas_dia = st.number_input("Horas de Trabalho por Dia", value=6)

# Cálculos de custos fixos e hora
total_fixo = salario + aluguel + transporte
total_horas = dias * horas_dia
custo_hora = total_fixo / total_horas if total_horas > 0 else 0
custo_materiais = 15.76  # Insumos fixos padrão

st.divider()

st.subheader("📝 Dados do Atendimento")
procedimento = st.text_input("Nome do Procedimento / Região", placeholder="Ex: Conch, Helix, Nostril...")
tempo_horas = st.slider("Tempo estimado de atendimento (Horas)", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
valor_joia = st.number_input("Custo da Joia (R$)", min_value=0.0, value=0.0, step=5.0)

# Taxas e Margem fixas validadas
retencao_total = 0.2699  # 20% lucro + 6.99% taxa cartão 3x sem juros

# Cálculo do Custo Operacional e Preço Final
custo_tempo = tempo_horas * custo_hora
custo_perfuracao = custo_materiais + custo_tempo + valor_joia
preco_ideal = custo_perfuracao / (1 - retencao_total)
lucro_estimado = preco_ideal * 0.20

st.divider()

# Exibição dos Resultados em destaque
st.subheader("💡 Resultado da Precificação")

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Custo Operacional Total", value=f"R$ {custo_perfuracao:.2f}")
with col2:
    st.metric(label="Lucro Líquido Estúdio (20%)", value=f"R$ {lucro_estimado:.2f}")

st.markdown(f"""
<div style="background-color: #1f2937; padding: 20px; border-radius: 10px; border-left: 5px solid #10b981; text-align: center; margin-top: 15px;">
    <h3 style="color: #9ca3af; margin:0;">VALOR IDEAL A COBRAR DA CLIENTE</h3>
    <h1 style="color: #10b981; font-size: 40px; margin: 5px 0;">R$ {preco_ideal:.2f}</h1>
    <p style="color: #d1d5db; font-size: 14px; margin:0;">Inclui taxa de cartão (3x) e garante 20% de lucro líquido real.</p>
</div>
""", unsafe_allow_html=True)

# Mensagem pronta para o WhatsApp
mensagem_whatsapp = f"""*Orçamento - Cat Piercer* 💎
Procedimento: {procedimento if procedimento else 'Personalizado'}
Valor do Investimento: *R$ {preco_ideal:.2f}*
Forma de pagamento: À vista no Pix ou parcelado em até 3x sem juros no cartão! ✨"""

st.markdown("---")
st.text_area("Copiar mensagem para enviar à cliente:", value=mensagem_whatsapp)
