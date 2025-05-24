import streamlit as st
from urllib.parse import unquote

# ===== Função para pegar parâmetros da URL =====
def get_query_param(key, default=""):
    try:
        query_params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
        value = query_params.get(key, [default])[0]
        return value if value not in [None, "", "null", "None"] else default
    except Exception:
        return default

def safe_float(x, default=2.00):
    try:
        if isinstance(x, str):
            x = x.replace(",", ".").strip()
        val = float(x)
        return val if val >= 1.01 else default
    except Exception:
        return default

def safe_str(x, default=""):
    return unquote(x) if x not in [None, "", "null", "None"] else default

# --- Inicializa campos apenas uma vez por sessão ---
if 'initialized' not in st.session_state:
    st.session_state['evento'] = safe_str(get_query_param("evento", ""))
    st.session_state['odds_a'] = safe_float(get_query_param("oddsA", 2.00))
    st.session_state['odds_b'] = safe_float(get_query_param("oddsB", 2.00))
    st.session_state['casa_a'] = safe_str(get_query_param("casaA", ""))
    st.session_state['casa_b'] = safe_str(get_query_param("casaB", ""))
    st.session_state['valor_total'] = 100
    st.session_state['initialized'] = True

# ===== Exibe logo + nome =====
col1, col2 = st.columns([1, 5])
with col1:
    st.image("logo.png", width=90)
with col2:
    st.markdown("""
        <h1 style='color:#1a3b5d; font-size:2.6em; font-weight:800; margin-bottom:0;'>ArbiFIFA <span style="color:#44cc77;">Pro</span></h1>
        <h4 style='color:gray; margin-top:0;'>Calculadora de Surebet 2 vias</h4>
    """, unsafe_allow_html=True)

evento = st.session_state['evento']
if evento:
    st.markdown(f"<div style='background:#eafbee;padding:8px 18px;border-radius:8px;font-size:1.2em'><b>Jogo:</b> {evento}</div>", unsafe_allow_html=True)

st.write("Preencha as odds e o nome das casas, ou use o link automático do sinal.")

col_odd_a, col_casa_a = st.columns([2, 3])
with col_odd_a:
    odds_a = st.number_input(
        "Odd",
        min_value=1.01,
        value=st.session_state['odds_a'],
        step=0.01,
        format="%.2f",
        key="odd_a"
    )
with col_casa_a:
    casa_a = st.text_input(
        "Casa",
        value=st.session_state['casa_a'],
        key="casa_a"
    )

col_odd_b, col_casa_b = st.columns([2, 3])
with col_odd_b:
    odds_b = st.number_input(
        "Odd",
        min_value=1.01,
        value=st.session_state['odds_b'],
        step=0.01,
        format="%.2f",
        key="odd_b"
    )
with col_casa_b:
    casa_b = st.text_input(
        "Casa",
        value=st.session_state['casa_b'],
        key="casa_b"
    )

valor_total = st.number_input(
    "Valor total para apostar (apenas inteiros)",
    min_value=1,
    value=st.session_state['valor_total'],
    step=1,
    format="%d",
    key="valor_total"
)

# ===== Cálculo Surebet CORRETO ====
surebet_percent = (1/odds_a + 1/odds_b) * 100
lucro_percent = 100 - surebet_percent
is_surebet = surebet_percent < 100

# Aposta ideal em cada casa
aposta_a = valor_total / (1 + (odds_a / odds_b))
aposta_b = valor_total - aposta_a

aposta_a_int = int(round(aposta_a))
aposta_b_int = int(round(aposta_b))

# Lucro em reais — sempre fixo pela fórmula
lucro_reais = int(round(valor_total * lucro_percent / 100))

# ==== APRESENTAÇÃO =====
st.markdown("### Resultado do cálculo")
if is_surebet:
    st.success(f"✅ **Surebet encontrada!**")
    colA, colB = st.columns(2)
    with colA:
        st.markdown(f"""
            <div style='background:#eafbee;border-radius:9px;padding:12px;text-align:center;margin-bottom:10px;'>
                <b style='font-size:1.3em; color:#1a3b5d'>{casa_a or "Casa A"}</b><br>
                <span style='font-size:1.15em;'>Odd <b>{odds_a:.2f}</b></span><br>
                <span style='color:#228B22; font-weight:bold; font-size:1.22em;'>Apostar R$ {aposta_a_int}</span>
            </div>
        """, unsafe_allow_html=True)
    with colB:
        st.markdown(f"""
            <div style='background:#eafbee;border-radius:9px;padding:12px;text-align:center;margin-bottom:10px;'>
                <b style='font-size:1.3em; color:#1a3b5d'>{casa_b or "Casa B"}</b><br>
                <span style='font-size:1.15em;'>Odd <b>{odds_b:.2f}</b></span><br>
                <span style='color:#228B22; font-weight:bold; font-size:1.22em;'>Apostar R$ {aposta_b_int}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown(f"""
        <div style='background:#fffbe6;border-radius:10px;padding:20px 10px 10px 10px;margin-top:5px;margin-bottom:10px;text-align:center'>
            <span style='font-size:2.6em; font-weight:bold; color:#096b2c;'>💰 R$ {lucro_reais}</span>
            <span style='font-size:2.2em; font-weight:800; color:#faad14; margin-left:18px;'>+{lucro_percent:.2f}%</span><br>
            <span style='font-size:1.1em; color:#333; font-weight:600; letter-spacing:0.3px'>Lucro garantido sobre o total apostado</span>
        </div>
    """, unsafe_allow_html=True)
else:
    st.error("❌ Não há surebet nessas odds.")

st.markdown("<hr><center><small>Desenvolvido por ArbiFIFA Pro © 2024</small></center>", unsafe_allow_html=True)
