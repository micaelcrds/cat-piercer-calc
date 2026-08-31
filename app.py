import streamlit as st

# Configuração da página
st.set_page_config(
    page_title="Cat Piercer - Precificação",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Estilo visual escuro moderno
st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .info-box { 
        background-color: #1f2937; 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #ff4b4b; 
        margin-top: 10px; 
        margin-bottom: 20px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

st.title("💎 Cat Piercer - Simulador de Preço")
st.markdown("Cálculo dinâmico com regras de repasse e parcelamento.")

with st.expander("⚙️ Parâmetros Fixos do Estúdio"):
  salario = st.number_input("Pró-labore", value=2500.0)
  aluguel = st.number_input("Custos Fixos", value=650.0)
  transporte = st.number_input("Transporte", value=288.0)
  dias = st.number_input("Dias no Mês", value=12)
  horas_dia = st.number_input("Horas/Dia", value=6)

# Custos Base (Tempo fixado em 1h exata)
custo_hora = (salario + aluguel + transporte) / (dias * horas_dia)
custo_operacional_base = 15.76 + custo_hora

st.subheader("📝 Dados do Atendimento")
procedimento = st.text_input(
    "Nome do Procedimento / Região", placeholder="Ex: Conch, Helix, Nostril..."
)
valor_joia = st.number_input(
    "Custo da Joia (R$)", min_value=0.0, value=0.0, step=5.0
)

# Taxas extraídas da máquina
tx_1x_total = 0.0419
tx_repasse = {
    2: 0.0248,
    3: 0.0339,
    4: 0.1136,
    5: 0.1431,
    6: 0.1432
}

custo_total = custo_operacional_base + valor_joia

# Verifica se o preço final absorvendo a taxa de 3x chega a R$ 100
preco_teste_3x = custo_total / (1 - 0.20 - 0.0699)

st.divider()
st.subheader("💡 Resultado da Precificação")

if preco_teste_3x >= 100.0:
    preco_base = preco_teste_3x
    
    st.markdown(f"""
    <div class="info-box" style="border-left-color: #10b981;">
        <h4 style="margin:0; color:#10b981;">💰 COMPRA DE R$ 100 OU MAIS</h4>
        <p style="margin:5px 0 0 0; font-size:14px; color:#d1d5db;">O valor absorve a taxa de 3x sem juros (6,99%).<br>
        Na máquina, digite <b>R$ {preco_base:.2f}</b>. Para 4x, 5x ou 6x, <b>ative a chave de repasse</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\nProcedimento: {procedimento if procedimento else 'Personalizado'}\n\n"
    msg += f"✨ *Valor: R$ {preco_base:.2f}*\n"
    msg += f"(Aceitamos Pix ou Cartão de Crédito em até 3x sem juros de R$ {preco_base/3:.2f})\n\n"
    msg += "Opções para parcelamento estendido:\n"
    for i in range(4, 7):
        total_cliente = preco_base * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n"
        
else:
    preco_pix = custo_total / (1 - 0.20)
    preco_1x = custo_total / (1 - 0.20 - tx_1x_total)
    
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin:0; color:#ff4b4b;">📉 COMPRA ABAIXO DE R$ 100</h4>
        <p style="margin:5px 0 0 0; font-size:14px; color:#d1d5db;">Sem parcelamento sem juros. Há variação entre Pix e Cartão.<br>
        Na máquina, digite <b>R$ {preco_1x:.2f}</b>. Se a cliente parcelar (2x a 6x), <b>ative a chave de repasse</b>.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\nProcedimento: {procedimento if procedimento else 'Personalizado'}\n\n"
    msg += f"✨ *Pix: R$ {preco_pix:.2f}*\n"
    msg += f"💳 *Cartão (1x): R$ {preco_1x:.2f}*\n\n"
    msg += "Opções de parcelamento no Cartão:\n"
    for i in range(2, 7):
        total_cliente = preco_1x * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n"

st.text_area("Copiar mensagem para o WhatsApp:", value=msg, height=300)