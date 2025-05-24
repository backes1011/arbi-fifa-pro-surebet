import streamlit as st
import math
from urllib.parse import unquote

# ====== Função para pegar parâmetros da URL ======
def get_query_param(key, default=""):
    return st.experimental_get_query_params().get(key, [default])[0]

# ====== Parâmetros recebidos via URL ======
evento = get_query_param("evento")
oddsA_url = get_query_param("oddsA")
oddsB_url = get_query_param("oddsB")
casaA_url = get_query_param("casaA")
casaB_url = get_query_param("casaB")

# ===== Exibe logo + nome =====
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=90)
with col2:
    st.markdown("""
        <h1 style='color:#1a3b5d; font-size:2.6em; font-weight:800; margin-bottom:0;'>ArbiFIFA <span style="color:#44cc77;">Pro</span></h1>
        <h4 style='color:gray; margin-top:0;'>Calculadora de Surebet 2 vias</h4>
    """, unsafe_allow_html=True)

# ==== Se veio pelo link de sinal, exibe o evento em destaque ====
if evento:
    st.markdown(f"<div style='background:#eafbee;padding:8px 18px;border-radius:8px;font-size:1.2em'><b>Jogo:</b> {unquote(evento)}</div>", unsafe_allow_html=True)

# ==== Campos de entrada já preenchidos pelo link ====
casa_a = st.text_input("Nome da Casa A", value=unquote(casaA_url) if casaA_url else "Casa A")
casa_b = st.text_input("Nome da Casa B", value=unquote(casaB_url) if casaB_url else "Casa B")
odds_a = st.number_input(f"Odd {casa_a}", min_value=1.01, value=float(oddsA_url) if oddsA_url else 2.00, step=0.01, format="%.2f")
odds_b = st.number_input(f"Odd {casa_b}", min_value=1.01, value=float(oddsB_url) if oddsB_url else 2.00, step=0.01, format="%.2f")
valor_total = st.number_input("Valor total para apostar (apenas inteiros)", min_value=1, value=100, step=1, format="%d")

# ===== Cálculo Surebet =====
surebet_percent = (1/odds_a + 1/odds_b) * 100
is_surebet = surebet_percent < 100

aposta_a = valor_total / (1 + (odds_a / odds_b))
aposta_b = valor_total - aposta_a

aposta_a_int = int(round(aposta_a))
aposta_b_int = int(round(aposta_b))

lucro_percent = 100 - surebet_percent
lucro_reais = int(round(valor_total * (lucro_percent/100)))

# ==== Lucro Destacado e Caixa Bonita ====
st.markdown("### Resultado do cálculo")
if is_surebet:
    st.success(f"✅ **Surebet encontrada!**")
    st.write(f"• Apostar **R$ {aposta_a_int}** em **{casa_a}** (Odd {odds_a})")
    st.write(f"• Apostar **R$ {aposta_b_int}** em **{casa_b}** (Odd {odds_b})")
    st.markdown(f"""
        <div style='background:#fffbe6;border-radius:10px;padding:20px 10px 10px 10px;margin-top:18px;margin-bottom:10px;text-align:center'>
            <span style='font-size:2.6em; font-weight:bold; color:#096b2c;'>💰 R$ {lucro_reais}</span>
            <span style='font-size:2.2em; font-weight:800; color:#faad14; margin-left:18px;'>+{lucro_percent:.2f}%</span><br>
            <span style='font-size:1.1em; color:#333; font-weight:600; letter-spacing:0.3px'>Lucro garantido sobre o total apostado</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Não há surebet nessas odds.")

# Rodapé
st.markdown("<hr><center><small>Desenvolvido por ArbiFIFA Pro © 2024</small></center>", unsafe_allow_html=True)
