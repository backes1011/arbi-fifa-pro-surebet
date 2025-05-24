import streamlit as st
from urllib.parse import unquote

# ====== Função para pegar parâmetros da URL ======
def get_query_param(key, default=""):
    try:
        # Prefer st.query_params se existir, senão fallback para experimental
        query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
        return query_params.get(key, [default])[0]
    except Exception:
        return default

def safe_float(x, default=2.00):
    try:
        if isinstance(x, str):
            x = x.replace(",", ".").strip()
        return float(x)
    except Exception:
        return default

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

# ==== Entradas: Casa + Odd lado a lado ====
st.write("Preencha as odds e o nome das casas, ou use o link automático do sinal.")

col_odd_a, col_casa_a = st.columns([2, 3])
with col_odd_a:
    odds_a = st.number_input(
        "Odd",
        min_value=1.01,
        value=safe_float(oddsA_url, 2.00),
        step=0.01,
        format="%.2f",
        key="odd_a"
    )
with col_casa_a:
    casa_a = st.text_input(
        "Casa",
        value=unquote(casaA_url) if casaA_url else "Casa A",
        key="casa_a"
    )

col_odd_b, col_casa_b = st.columns([2, 3])
with col_odd_b:
    odds_b = st.number_input(
        "Odd",
        min_value=1.01,
        value=safe_float(oddsB_url, 2.00),
        step=0.01,
        format="%.2f",
        key="odd_b"
    )
with col_casa_b:
    casa_b = st.text_input(
        "Casa",
        value=unquote(casaB_url) if casaB_url else "Casa B",
        key="casa_b"
    )

valor_total = st.number_input(
    "Valor total para apostar (apenas inteiros)",
    min_value=1,
    value=100,
    step=1,
    format="%d"
)

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
