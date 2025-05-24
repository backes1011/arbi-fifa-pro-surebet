import streamlit as st
from urllib.parse import unquote

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

# Leitura dos parâmetros via URL (campos ocultos para URL)
oddA_url = st.text_input("Odd A (URL)", value=get_query_param("oddsA", ""), key="url_oddsA", type="default", label_visibility="collapsed")
oddB_url = st.text_input("Odd B (URL)", value=get_query_param("oddsB", ""), key="url_oddsB", type="default", label_visibility="collapsed")
casaA_url = st.text_input("Casa A (URL)", value=get_query_param("casaA", ""), key="url_casaA", type="default", label_visibility="collapsed")
casaB_url = st.text_input("Casa B (URL)", value=get_query_param("casaB", ""), key="url_casaB", type="default", label_visibility="collapsed")
evento_url = st.text_input("Evento (URL)", value=get_query_param("evento", ""), key="url_evento", type="default", label_visibility="collapsed")

if 'initialized' not in st.session_state:
    st.session_state['evento'] = safe_str(evento_url)
    st.session_state['odds_a'] = safe_float(oddA_url, 2.00)
    st.session_state['odds_b'] = safe_float(oddB_url, 2.00)
    st.session_state['casa_a'] = safe_str(casaA_url)
    st.session_state['casa_b'] = safe_str(casaB_url)
    st.session_state['valor_total'] = 100
    st.session_state['initialized'] = True

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
    value=int(st.session_state['valor_total']),
    step=1,
    format="%d",
    key="valor_total"
)

# CALCULO TEÓRICO DO PERCENTUAL (fixo, para as odds)
surebet_percent = (1/odds_a + 1/odds_b) * 100
lucro_percent_teorico = 100 - surebet_percent
is_surebet = surebet_percent < 100

# Valores a apostar (inteiros, arredondados para baixo)
aposta_a = valor_total / (1 + (odds_a / odds_b))
aposta_a_int = int(aposta_a)
aposta_b_int = valor_total - aposta_a_int

# Retornos reais (com valores inteiros)
retorno_a = aposta_a_int * odds_a
retorno_b = aposta_b_int * odds_b
lucro_a = retorno_a - valor_total
lucro_b = retorno_b - valor_total
lucro_real = min(lucro_a, lucro_b)
lucro_percent_real = (lucro_real / valor_total) * 100 if valor_total > 0 else 0

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
            <span style='font-size:2.6em; font-weight:bold; color:#096b2c;'>💰 R$ {lucro_real:.2f}</span>
            <span style='font-size:2.2em; font-weight:800; color:#faad14; margin-left:18px;'>+{lucro_percent_teorico:.2f}%</span><br>
            <span style='font-size:1.1em; color:#333; font-weight:600; letter-spacing:0.3px'>Lucro garantido sobre o total apostado (teórico para as odds)</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<center><small>Obs: O valor em R$ é calculado com os valores inteiros. O percentual é sempre o teórico das odds.</small></center>", unsafe_allow_html=True)
else:
    st.error("❌ Não há surebet nessas odds.")

st.markdown("<hr><center><small>Desenvolvido por ArbiFIFA Pro © 2024</small></center>", unsafe_allow_html=True)
