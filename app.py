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

# Leitura inicial dos parâmetros via URL
odds_a_url = get_query_param("oddsA", "")
odds_b_url = get_query_param("oddsB", "")
casa_a_url = get_query_param("casaA", "")
casa_b_url = get_query_param("casaB", "")

if 'initialized' not in st.session_state:
    st.session_state['odds_a'] = safe_float(odds_a_url, 2.00)
    st.session_state['odds_b'] = safe_float(odds_b_url, 2.00)
    st.session_state['casa_a'] = safe_str(casa_a_url)
    st.session_state['casa_b'] = safe_str(casa_b_url)
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

st.write("Preencha as odds e o nome das casas, ou use o link automático do sinal.")

col_odd_a, col_casa_a = st.columns(2)
with col_odd_a:
    odds_a = st.number_input(
        "Odd A",
        min_value=1.01,
        value=st.session_state['odds_a'],
        step=0.01,
        format="%.2f",
        key="odd_a"
    )
with col_casa_a:
    casa_a = st.text_input(
        "Casa A",
        value=st.session_state['casa_a'],
        key="casa_a"
    )

col_odd_b, col_casa_b = st.columns(2)
with col_odd_b:
    odds_b = st.number_input(
        "Odd B",
        min_value=1.01,
        value=st.session_state['odds_b'],
        step=0.01,
        format="%.2f",
        key="odd_b"
    )
with col_casa_b:
    casa_b = st.text_input(
        "Casa B",
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

# --- Percentual teórico, SEMPRE fixo para as odds ---
surebet_percent = (1/odds_a + 1/odds_b) * 100
lucro_percent_teorico = 100 - surebet_percent
is_surebet = surebet_percent < 100

# --- Cálculo dos valores a apostar (arredondado para baixo) ---
aposta_a = valor_total / (1 + (odds_a / odds_b))
aposta_a_int = int(aposta_a)
aposta_b_int = valor_total - aposta_a_int

# --- Retornos de cada casa (com apostas inteiras) ---
retorno_a = aposta_a_int * odds_a
retorno_b = aposta_b_int * odds_b
lucro_a = retorno_a - valor_total
lucro_b = retorno_b - valor_total

# Percentual de lucro real para cada casa (não exibido em destaque, só como referência na tabela)
lucro_a_percent = (lucro_a / valor_total) * 100
lucro_b_percent = (lucro_b / valor_total) * 100

# Lucro garantido mínimo (igual BetBurger)
lucro_real = min(lucro_a, lucro_b)

# ---------- Apresentação igual BetBurger -----------
# Percentual teórico no topo
st.markdown(f"""
    <div style='display:flex;align-items:center;justify-content:left;gap:18px; margin-bottom:12px;'>
        <div style='background:#f5f7fb;border-radius:8px;padding:12px 22px;font-size:2.1em; font-weight:900; color:#138e52;letter-spacing:0.5px;'>
            {lucro_percent_teorico:.2f}% 
        </div>
        <div style='font-size:1.22em;color:#868686;'>Lucro percentual teórico</div>
    </div>
""", unsafe_allow_html=True)

st.markdown("### Resultado do cálculo")
if is_surebet:
    st.success(f"✅ **Surebet encontrada!**")

    st.markdown(
        "<div style='display:flex;gap:16px;'>"
        f"<div style='background:#eafbee;border-radius:12px;padding:18px 28px 12px 28px;width: 50%;text-align:center;'><b style='font-size:1.25em;color:#1a3b5d'>{casa_a or 'Casa A'}</b><br>"
        f"Odd <b>{odds_a:.2f}</b><br>"
        f"Apostar <b style='color:#228B22;font-size:1.17em;'>R$ {aposta_a_int}</b><br>"
        f"<span style='font-size:1.1em;'>Lucro se vencer:<br>"
        f"<b style='color:#096b2c;'>R$ {lucro_a:.2f}</b> &nbsp; <span style='color:#faad14;'>{lucro_a_percent:.2f}%</span></span></div>"
        f"<div style='background:#eafbee;border-radius:12px;padding:18px 28px 12px 28px;width: 50%;text-align:center;'><b style='font-size:1.25em;color:#1a3b5d'>{casa_b or 'Casa B'}</b><br>"
        f"Odd <b>{odds_b:.2f}</b><br>"
        f"Apostar <b style='color:#228B22;font-size:1.17em;'>R$ {aposta_b_int}</b><br>"
        f"<span style='font-size:1.1em;'>Lucro se vencer:<br>"
        f"<b style='color:#096b2c;'>R$ {lucro_b:.2f}</b> &nbsp; <span style='color:#faad14;'>{lucro_b_percent:.2f}%</span></span></div>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(f"""
        <div style='background:#fffbe6;border-radius:10px;padding:20px 10px 10px 10px;margin-top:18px;margin-bottom:10px;text-align:center'>
            <span style='font-size:2.6em; font-weight:bold; color:#096b2c;'>💰 R$ {lucro_real:.2f}</span>
            <span style='font-size:2.2em; font-weight:800; color:#faad14; margin-left:18px;'>({lucro_percent_teorico:.2f}%)</span><br>
            <span style='font-size:1.1em; color:#333; font-weight:600; letter-spacing:0.3px'>Lucro garantido (mínimo entre as casas) — Percentual sempre fixo!</span>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(
        f"<center><small>O percentual no topo e abaixo é sempre o teórico das odds, igual BetBurger. O valor em R$ é garantido, usando apostas inteiras. Lucro em cada casa é exibido para consulta, mas o garantido é sempre o menor dos dois.</small></center>",
        unsafe_allow_html=True
    )
else:
    st.error("❌ Não há surebet nessas odds.")

st.markdown("<hr><center><small>Desenvolvido por ArbiFIFA Pro © 2024</small></center>", unsafe_allow_html=True)
