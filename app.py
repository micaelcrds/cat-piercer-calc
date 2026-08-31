import streamlit as st
import math
import os
import base64

# Configuração da página
st.set_page_config(
    page_title="Cat Piercer - Precificação",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def truncar_dez_centavos(valor):
    """Arredonda o valor para baixo cortando os centavos finais (ex: 87.29 vira 87.20)"""
    return math.floor(valor * 10) / 10.0

def renderizar_logo_cartao(caminho_imagem="logo.png"):
    """Força o alinhamento central absoluto usando Flexbox HTML/CSS"""
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        
        st.markdown(
            f"""
            <div style="display: flex; justify-content: center; width: 100%; margin-bottom: 10px;">
                <div style="
                    background-color: #ffffff;
                    padding: 15px 25px;
                    border-radius: 16px;
                    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
                    display: flex;
                    justify-content: center;
                    align-items: center;
                ">
                    <img src="data:image/png;base64,{b64}" alt="Cat Piercer Logo" style="max-height: 120px; width: auto; mix-blend-mode: multiply; filter: none;">
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.warning("⚠️ Imagem não encontrada. Verifique se o arquivo se chama 'logo.png' no GitHub.")

# Estilos CSS
st.markdown(
    """
    <style>
    .info-box { 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #ff4b4b; 
        margin-top: 10px; 
        margin-bottom: 20px;
        background-color: rgba(128, 128, 128, 0.1);
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Renderiza a logo
renderizar_logo_cartao("logo.png")

st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Simulador de Preço</h3>", unsafe_allow_html=True)

with st.expander("⚙️ Parâmetros Fixos do Estúdio"):
    salario = st.number_input("Pró-labore (Salário mensal livre desejado)", value=2500.0)
    aluguel = st.number_input("Custos Fixos (Aluguel, Água, Luz, Internet, etc.)", value=650.0)
    transporte = st.number_input("Transporte (Gasto mensal com locomoção)", value=288.0)
    dias = st.number_input("Dias no Mês (Quantos dias o estúdio abre no mês)", value=12)
    horas_dia = st.number_input("Horas/Dia (Carga horária diária de trabalho)", value=6)

custo_hora = (salario + aluguel + transporte) / (dias * horas_dia)
custo_operacional_base = 15.76 + custo_hora

st.subheader("📝 Dados do Atendimento")
procedimento = st.text_input("Nome do Procedimento", placeholder="Ex: Conch, Helix, Nostril...")

# --- SISTEMA DINÂMICO DE JOIAS ---
st.markdown("#### 💎 Joias Utilizadas")

# Inicializa o contador de tipos de joias na memória da página
if 'qtd_tipos_joias' not in st.session_state:
    st.session_state.qtd_tipos_joias = 1

custo_total_joias = 0
info_joias_list = []

# Gera os campos para cada joia dinamicamente
for i in range(st.session_state.qtd_tipos_joias):
    with st.container():
        st.markdown(f"**Item {i+1}**")
        col1, col2 = st.columns([2, 1])
        with col1:
            nome = st.text_input(f"Nome da Joia", placeholder="Ex: Argola Titânio...", key=f"nome_{i}")
        with col2:
            qtd = st.number_input(f"Quantidade", min_value=1, value=1, step=1, key=f"qtd_{i}")
        
        valor = st.number_input(f"Custo Unitário da Joia (R$)", min_value=0.0, value=0.0, step=5.0, key=f"valor_{i}")
        st.markdown("---")
        
        custo_total_joias += (valor * qtd)
        
        if nome:
            info_joias_list.append(f"{qtd}x {nome}")
        elif valor > 0:
            info_joias_list.append(f"{qtd}x Joia Padrão")

# Botões para adicionar ou remover itens
colA, colB = st.columns(2)
with colA:
    if st.button("➕ Adicionar outra joia"):
        st.session_state.qtd_tipos_joias += 1
        st.rerun()
with colB:
    if st.session_state.qtd_tipos_joias > 1:
        if st.button("❌ Remover última"):
            st.session_state.qtd_tipos_joias -= 1
            st.rerun()
# ---------------------------------

custo_total = custo_operacional_base + custo_total_joias

# Taxas
margem = 0.20
tx_1x_total = 0.0419
tx_3x_absorvida = 0.0699

tx_repasse = {
    2: 0.0964,
    3: 0.1123,
    4: 0.1136,
    5: 0.1431,
    6: 0.1432
}

preco_teste = custo_total / (1 - margem - tx_3x_absorvida)
preco_teste_truncado = truncar_dez_centavos(preco_teste)

st.divider()
st.subheader("💡 Resultado da Precificação")

# Preparação das joias em formato de tópicos para o WhatsApp
info_joia_str = ""
if info_joias_list:
    info_joia_str = "💍 *Joias inclusas:*\n"
    for joia in info_joias_list:
        info_joia_str += f" ▫️ {joia}\n"

if preco_teste_truncado >= 100.0:
    preco_base = preco_teste_truncado
    
    st.markdown(f"""
    <div class="info-box" style="border-left-color: #10b981;">
        <h4 style="margin:0; color:#10b981;">💰 COMPRA DE R$ 100 OU MAIS</h4>
        <p style="margin:5px 0 0 0; font-size:14px;">A taxa da máquina já está coberta para Pix ou parcelado até 3x.<br>
        Na máquina, digite <b>R$ {preco_base:.2f}</b> (Sem repasse). Acima de 3x, use a chave de repasse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\n\n"
    msg += f"📍 *Procedimento:* {procedimento if procedimento else 'Personalizado'}\n"
    if info_joias_list:
        msg += f"{info_joia_str}"
    msg += f"\n✨ *Investimento Total: R$ {preco_base:.2f}*\n\n"
    msg += f"💳 *Pagamento (Pix ou Cartão sem juros):*\n"
    msg += f"• À vista (Pix ou 1x no Cartão)\n"
    msg += f"• 2x de R$ {preco_base/2:.2f} sem juros\n"
    msg += f"• 3x de R$ {preco_base/3:.2f} sem juros\n\n"
    msg += f"🔄 *Parcelamento estendido (com acréscimo da maquininha):*\n"
    for i in range(4, 7):
        total_cliente = preco_base * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n"
        
else:
    preco_pix = truncar_dez_centavos(custo_total / (1 - margem))
    preco_1x = truncar_dez_centavos(custo_total / (1 - margem - tx_1x_total))
    
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin:0; color:#ff4b4b;">📉 COMPRA ABAIXO DE R$ 100</h4>
        <p style="margin:5px 0 0 0; font-size:14px;">Os valores mudam para absorver as taxas específicas.<br>
        Na máquina, digite <b>R$ {preco_1x:.2f}</b>. Se a cliente quiser parcelar (2x ou 3x), ative a chave de repasse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\n\n"
    msg += f"📍 *Procedimento:* {procedimento if procedimento else 'Personalizado'}\n"
    if info_joias_list:
        msg += f"{info_joia_str}"
    msg += f"\n✨ *Investimento (Pix): R$ {preco_pix:.2f}*\n"
    msg += f"💳 *Investimento (Cartão 1x): R$ {preco_1x:.2f}*\n\n"
    msg += f"🔄 *Opções de parcelamento no Cartão:*\n"
    for i in range(2, 4):
        total_cliente = preco_1x * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n"

st.text_area("Copiar mensagem para o WhatsApp:", value=msg, height=450)