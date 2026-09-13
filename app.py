import streamlit as st
import math
import os
import base64

st.set_page_config(
    page_title="Cat Piercer - Precificação",
    page_icon="💎",
    layout="centered",
    initial_sidebar_state="collapsed",
)

def truncar_dez_centavos(valor):
    """Arredonda o valor para baixo cortando os centavos finais"""
    return math.floor(valor * 10) / 10.0

def renderizar_logo_cartao(caminho_imagem="logo.png"):
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
    .item-container {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    </style>
""",
    unsafe_allow_html=True,
)

renderizar_logo_cartao("logo.png")

st.markdown("<h3 style='text-align: center; margin-top: 10px;'>Simulador de Preço</h3>", unsafe_allow_html=True)

st.subheader("📝 Dados do Atendimento")
procedimento = st.text_input("Nome do Procedimento", placeholder="Ex: Conch, Helix, Nostril...")

st.markdown("#### 💎 Joias e Categorias")

if 'qtd_tipos_joias' not in st.session_state:
    st.session_state.qtd_tipos_joias = 1

preco_sugerido_total = 0
total_joias_unidades = 0
info_joias_list = []

for i in range(st.session_state.qtd_tipos_joias):
    st.markdown(f"<div class='item-container'>", unsafe_allow_html=True)
    st.markdown(f"**Item {i+1}**")
    
    nome = st.text_input(f"Nome da Joia", placeholder="Ex: Argola Titânio...", key=f"nome_{i}")
    categoria = st.selectbox(
        "Categoria do Procedimento", 
        ["Perfuração (+ R$ 70)", "Atualização (+ R$ 25)", "Venda de Joia (+ R$ 0)"],
        key=f"cat_{i}"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        valor = st.number_input(f"Custo da Joia (R$)", min_value=0.0, value=0.0, step=5.0, key=f"valor_{i}")
    with col2:
        qtd = st.number_input(f"Quantidade", min_value=1, value=1, step=1, key=f"qtd_{i}")
    
    if "Perfuração" in categoria:
        markup = 70.0
    elif "Atualização" in categoria:
        markup = 25.0
    else:
        markup = 0.0
        
    preco_item = (valor + markup) * qtd
    preco_sugerido_total += preco_item
    total_joias_unidades += qtd
    
    nome_exibicao = nome if nome else f"Joia ({categoria.split(' ')[0]})"
    info_joias_list.append(f"{qtd}x {nome_exibicao} — R$ {preco_item:.2f}")
        
    st.markdown("</div>", unsafe_allow_html=True)

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

st.divider()
st.subheader("💡 Resultado da Precificação")

desconto_percentual = 0.0
if total_joias_unidades == 2:
    desconto_percentual = 0.15
elif total_joias_unidades >= 3:
    desconto_percentual = 0.20

usar_desconto = False
if desconto_percentual > 0:
    st.info("Múltiplas joias detectadas! O desconto combo será aplicado sobre o valor final de venda.")
    usar_desconto = st.checkbox(f"🎁 Aplicar Desconto Combo ({int(desconto_percentual*100)}% para {int(total_joias_unidades)} joias)", value=True)

if usar_desconto:
    preco_final = truncar_dez_centavos(preco_sugerido_total * (1 - desconto_percentual))
    texto_investimento = f"De ~R$ {preco_sugerido_total:.2f}~ por *R$ {preco_final:.2f}*"
else:
    preco_final = truncar_dez_centavos(preco_sugerido_total)
    texto_investimento = f"*R$ {preco_final:.2f}*"

preco_pix = truncar_dez_centavos(preco_final * 0.95)

info_joia_str = ""
if info_joias_list:
    info_joia_str = "\n💍 *Joias inclusas:*\n"
    for joia in info_joias_list:
        info_joia_str += f" ▫️ {joia}\n"

texto_inclusoes = """
*Inclui:*
* Perfuração 
* Joia em Titânio 
* Material Estéril e Descartável 
* Anodização (mudança de cor da joia)
* Kit de Primeiros Cuidados
* Cartão Fidelidade
* Retornos online ilimitados e presenciais até 45 dias
* *⁠_Novidade:_*
    Downsize (redução de haste) cortesia, até 60 dias.

Qual seria a melhor opção para você no momento? 🥰💜"""

tx_repasse = {2: 0.0964, 3: 0.1123, 4: 0.1136, 5: 0.1431, 6: 0.1432}

if preco_final >= 100.0:
    st.markdown(f"""
    <div class="info-box" style="border-left-color: #10b981;">
        <h4 style="margin:0; color:#10b981;">💰 COMPRA DE R$ 100 OU MAIS</h4>
        <p style="margin:5px 0 0 0; font-size:14px;">Você absorve as taxas até 3x para facilitar a venda.<br>
        Na máquina, digite <b>R$ {preco_final:.2f}</b> (Sem repasse). Acima de 3x, use a chave de repasse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\n\n"
    msg += f"📍 *Procedimento:* {procedimento if procedimento else 'Personalizado'}\n"
    if info_joias_list:
        msg += f"{info_joia_str}"
    msg += f"\n✨ *Investimento Total:* {texto_investimento}\n\n"
    msg += f"💳 *Formas de Pagamento:*\n"
    msg += f"• Pix *(5% OFF)*: R$ {preco_pix:.2f}\n"
    msg += f"• 1x no Cartão: R$ {preco_final:.2f}\n"
    msg += f"• 2x de R$ {preco_final/2:.2f} sem juros\n"
    msg += f"• 3x de R$ {preco_final/3:.2f} sem juros\n\n"
    msg += f"🔄 *Parcelamento estendido (com acréscimo da maquininha):*\n"
    for i in range(4, 7):
        total_cliente = preco_final * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n\n"
    msg += texto_inclusoes
        
else:
    st.markdown(f"""
    <div class="info-box">
        <h4 style="margin:0; color:#ff4b4b;">📉 COMPRA ABAIXO DE R$ 100</h4>
        <p style="margin:5px 0 0 0; font-size:14px;">Repasse obrigatório para compras parceladas.<br>
        Na máquina, digite <b>R$ {preco_final:.2f}</b>. Para 2x ou 3x, ative a chave de repasse.</p>
    </div>
    """, unsafe_allow_html=True)
    
    msg = f"*Orçamento - Cat Piercer* 💎\n\n"
    msg += f"📍 *Procedimento:* {procedimento if procedimento else 'Personalizado'}\n"
    if info_joias_list:
        msg += f"{info_joia_str}"
    msg += f"\n✨ *Investimento:* {texto_investimento}\n\n"
    msg += f"💳 *Formas de Pagamento:*\n"
    msg += f"• Pix *(5% OFF)*: R$ {preco_pix:.2f}\n"
    msg += f"• 1x no Cartão: R$ {preco_final:.2f}\n\n"
    msg += f"🔄 *Opções de parcelamento no Cartão (com acréscimo da maquininha):*\n"
    for i in range(2, 4):
        total_cliente = preco_final * (1 + tx_repasse[i])
        msg += f"• {i}x de R$ {total_cliente/i:.2f} (Total: R$ {total_cliente:.2f})\n\n"
    msg += texto_inclusoes

st.markdown("Copie a mensagem abaixo para enviar à cliente:")
st.code(msg, language="markdown")
