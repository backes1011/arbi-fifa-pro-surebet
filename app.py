import streamlit as st
import math
from PIL import Image

# ===== Exibe logo + nome =====
col1, col2 = st.columns([1,5])
with col1:
    st.image("logo.png", width=90)
with col2:
    st.markdown("""
        <h1 style='color:#1a3b5d; font-size:2.6em; font-weight:800; margin-bottom:0;'>ArbiFIFA <span style="color:#44cc77;">Pro</span></h1>
        <h4 style='color:gray; margin-top:0;'>Calculadora de Surebet 2 vias</h4>
    """, unsafe_allow_html=True)

st.write("Preencha as odds e o valor total. O cálculo é feito apenas com números inteiros (sem centavos).")

# ===== Inputs principais =====
odds_a = st.number_input("Odd Casa A", min_value=1.01, value=2.00, step=0.01, format="%.2f")
odds_b = st.number_input("Odd Casa B", min_value=1.01, value=2.00, step=0.01, format="%.2f")
valor_total = st.number_input("Valor total para apostar (apenas inteiros)", min_value=1, value=100, step=1, format="%d")

# ===== Cálculo Surebet =====
surebet_percent = (1/odds_a + 1/odds_b) * 100
is_surebet = surebet_percent < 100

aposta_a = valor_total / (1 + (odds_a / odds_b))
aposta_b = valor_total - aposta_a

# Arredonda para inteiros
aposta_a_int = int(round(aposta_a))
aposta_b_int = int(round(aposta_b))

# Lucro Fixo
lucro_percent = 100 - surebet_percent
lucro_reais = int(round(valor_total * (lucro_percent/100)))

retorno_a = aposta_a_int * odds_a
retorno_b = aposta_b_int * odds_b

st.markdown("### Resultado do cálculo")
if is_surebet:
    st.success(f"✅ **Surebet encontrada!**")
    st.write(f"• Apostar **R$ {aposta_a_int}** na Odd A ({odds_a})")
    st.write(f"• Apostar **R$ {aposta_b_int}** na Odd B ({odds_b})")
    st.write(f"• **Retorno garantido:** R$ {int(min(retorno_a, retorno_b))}")
    st.write(f"• **Lucro garantido:** R$ {lucro_reais} (**{lucro_percent:.2f}%** sobre o total apostado)")
else:
    st.error("❌ Não há surebet nessas odds.")

# ====== Configuração Google Sheets + Instruções ======
st.markdown("---")
cols = st.columns([2, 2])
with cols[0]:
    st.markdown("### Configuração do Google Planilhas")
    planilha_id = st.text_input("ID da planilha do Google Sheets")
    credenciais_json = st.text_area("Credenciais do Google (cole aqui o JSON do serviço)")
    if st.button("Registrar entrada na Planilha"):
        st.info("⚠️ Integração com Google Sheets ainda não configurada neste protótipo.")
with cols[1]:
    st.markdown("""
    <div style='background-color:#f2f6fa; border-radius:8px; padding:18px 18px 5px 18px; font-size:0.98em'>
    <b>Como configurar?</b><br>
    1. Acesse <a href="https://console.cloud.google.com/" target="_blank">Google Cloud Console</a>.<br>
    2. Crie um projeto e ative a <b>Google Sheets API</b>.<br>
    3. Em "APIs e Serviços" &rarr; "Credenciais", crie uma credencial de <b>Conta de Serviço</b>.<br>
    4. Baixe o arquivo JSON e cole o conteúdo no campo acima.<br>
    5. Compartilhe sua planilha com o e-mail da conta de serviço.<br>
    6. O ID da planilha é o código no link: <br>
    <i>docs.google.com/spreadsheets/d/<b>SEU_ID_AQUI</b>/edit#gid=0</i>
    </div>
    """, unsafe_allow_html=True)

# Rodapé
st.markdown("<hr><center><small>Desenvolvido por ArbiFIFA Pro © 2024</small></center>", unsafe_allow_html=True)
