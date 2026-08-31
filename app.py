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

def renderizar_logo(caminho_imagem="logo.png"):
    """Renderiza duas versões da logo e usa CSS para alternar entre elas sem conflito com o OS"""
    if os.path.exists(caminho_imagem):
        with open(caminho_imagem, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <div class="logo-container">
                <!-- Versão Modo Claro -->
                <img class="logo-cat logo-light" src="data:image/png;base64,{b64}" alt="Cat Piercing Logo">
                <!-- Versão Modo Escuro -->
                <img class="logo-cat logo-dark" src="data:image/png;base64,{b64}" alt="Cat Piercing Logo">
            </div>
            """,
            unsafe_allow_html=True,
        )

# Estilos CSS Definitivos para blindar o tema
st.markdown(
    """
    <style>
    .logo-container {
        text-align: center;
        margin-bottom: 20px;
    }
    
    .logo-cat {
        max-width: 280px;
        width: 100%;
    }

    /* Estilos fixos de tratamento de cor da imagem */
    .logo-light {
        filter: none !important;
        mix-blend-mode: multiply !important;
    }
    
    .logo-dark {
        filter: invert(1) !important;
        mix-blend-mode: screen !important;
    }

    /* 1. COMPORTAMENTO PADRÃO DO SISTEMA OPERACIONAL */
    .logo-dark { display: none; }
    .logo-light { display: inline-block; }
    
    @media (prefers-color-scheme: dark) {
        .logo-light { display: none; }
        .logo-dark { display: inline-block; }
    }

    /* 2. OVERRIDE ABSOLUTO QUANDO O BOTÃO DO SITE FOR USADO */
    
    /* Se o usuário forçar o Tema Claro no site */
    [data-theme="light"] .logo-dark,
    .stApp[data-theme="light"] .logo-dark {
        display: none !important;
    }
    [data-theme="light"] .logo-light,
    .stApp[data-theme="light"] .logo-light {
        display: inline-block !important;
    }

    /* Se o usuário forçar o Tema Escuro no site */
    [data-theme="dark"] .logo-light,
    .stApp[data-theme="dark"] .logo-light {
        display: none !important;
    }
    [data-theme="dark"] .logo-dark,
    .stApp[data-theme="dark"] .logo-dark {
        display: inline-block !important;
    }

    .info-box { 
        padding: 15px; 
        border-radius: 8px; 
        border-left: 5px solid #ff4b4b; 
        margin-top: 10px; 
        margin-bottom: 20px;
        background-color: rgba(128, 128, 128, 0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Renderiza a logo blindada
renderizar_logo("logo.png")

st.markdown(
    "<h3 style='text-align: center; margin-top: -10px;'>Simulador de Preço</h3>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='text-align: center; color: gray; font-size: 14px;'>Cálculo cravado em 1h de atendimento com arredondamento inteligente.</p>",
    unsafe_allow_html=True,
)

with st.expander("⚙️ Parâmetros Fixos do Estúdio"):
    salario = st.number_input("Pró-labore", value=2500.0)
    aluguel = st.number_input("Custos Fixos", value=650.0)
    transporte = st.number_input("Transporte", value=288.0)
    dias = st.number_input("Dias no Mês", value=12)
    horas_dia = st.number_input("Horas/Dia", value=6)

custo_hora = (salario + aluguel + transporte) / (dias * horas_dia)
custo_operacional_base = 15.76 + custo_hora

st.subheader("📝 Dados do Atendimento")
procedimento = st.text_input(
    "Nome do Procedimento", placeholder="Ex: Conch, Helix, Nostril..."
)
valor_joia = st.number_input(
    "Custo da Joia (R$)", min_value=0.0, value=0.0, step=5.0
)

custo_total = custo_operacional_base + valor_joia

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

if preco_teste_truncado >= 100.0:
    preco_base = preco_teste_truncado
    
    st.markdown(f"""
    <div class="info-box" style="border-left-color: #10b981;">
        <h4 style="margin:0; color:#10b981;">💰 COMPRA DE R$ 100 OU MAIS</h4>
        <p style="margin:5px 0 0 0; font-size:14px;">A taxa da máquina já está coberta para Pix ou parcelado até 3x.<br>
        Na máquina, digite <b>R$ {preco_base:.2f}</b> (Sem repasse). Acima de 3x, use a chave de repasse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercing* 💎\nProcedimento: {procedimento if procedimento else 'Personalizado'}\n\n"
    msg += f"✨ *Valor: R$ {preco_base:.2f}*\n"
    msg += f"(Aceitamos Pix ou Cartão em até 3x sem juros!)\n"
    msg += f"• 2x sem juros de R$ {preco_base/2:.2f}\n"
    msg += f"• 3x sem juros de R$ {preco_base/3:.2f}\n\n"
    msg += "Opções para parcelamento estendido no Cartão:\n"
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
    
    msg = f"*Orçamento - Cat Piercing* 💎\nProcedimento: {procedimento if procedimento else 'Personalizado'}\n\n"
    msg += f"✨ *Pix: R$ {preco_pix:.2f}*\n"
    msg += f"💳 *Cartão (1x): R$ {preco_1x:.2f}*\n\n"
    msg += "Opções de parcelamento no Cartão:\n"
    for i in range(2, 4):
        total_cliente = preco_1x * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n"

st.text_area("Copiar mensagem para o WhatsApp:", value=msg, height=350)