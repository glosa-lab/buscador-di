import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Buscador DI", layout="wide")

st.title("📖 Buscador do Dicionário Informal")
st.markdown("Pesquisa morfológica — GREMD-USP (Dados de Dez/2025)")

# --- LISTA DE IDs ---
LISTA_DE_IDS = [
    "1u9Vp_jvbJE1GPWjyDzo59RE9geOcArWx", "1D1l2L4BnN5w2hmiqeWAOHT2mr3I-HMfg5bEgBjjgpcM",
    "1LWIoBHlxoYyBtU2Yviglmbr4z7PSz5qc", "1tr0GS4VoscbdwIoNN4YIhi5YyAtCkemR",
    "1hnqot_n9n55j09G1Yx-wktt1uPda8BFk", "1pltCsuDpDGpRNsAP_mmjPXgDF-dXaOLe",
    "1sJD-fyssg0zwA_hzSOyFt8ECx_6gV_4B", "1DMV-ywq-t6CJFICgTtP-7S_5Gl5ui421",
    "1zu_pjwwiffTPwJMAdcMYSb117zCAIGhc", "1-2-432yWisqasNDo0VJNPYXypnKut-7K",
    "1G2ZWyp3Ly_VP-fNwodLqRgmwSReCHWE-", "1BRo20jIzK_ZO8TPLUm78yrn_dbFm9X6F",
    "14_UdNb6HelhuhhxOyZpvQHS233YD1ll5", "1huRmAwRZ9FsA8Ei7yMGMQCkErkfEvQVL",
    "1ycSBsQR970tFuOV72bI91hoaHMjRQ4zeJShY0O_Y770", "1h6iGYYoq_DEUFeEa3Ss6hsRWYBAKkiE-Kdy7KB2OYs0",
    "1OzjPrgmtf6VHYiWhYcwMMSVz_Sv86XL0kzQVmK3s_hc", "1kBUgce7_Ik5i40p-Mfser69K6uFQEbBm-UJtcnnfPYA",
    "14jafTnXPSgI75CcbrCnxLnD8zkQKCsBd0PZ5A40nggE", "1Ir0Pmcg6PAaUfXNVxHcGy-pEr4VzyLW_JcPiwUbt0Z0",
    "1nigbsmbUoXwmOWPAEofRurzwtEQefOxEfk0LuZ6S65w", "1unSJHbz337YoKtpQPisQdeS5T8uetp_aIz6GyIXrplA",
    "1YbnbxgJdCOmioU2vhQkcOshhk6CkOB5l7D2rk6P1rDo", "1ZWozXE9_RrW8CyH9xiWxQmZ7oZwF5RsbWIRQKW-7Jk8",
    "1mvkNRiEQ7FXDNwknR5nq6V1gLYw3pHWFIG621xplabk", "1NotlOYE3H8HYLvrs9PUoqkcD_zoEWcGqQH8R-ciYqLE"
]

@st.cache_data(ttl=86400)
def carregar_corpus(ids):
    total_df = []
    for sheet_id in ids:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df_temp = pd.read_csv(url)
            total_df.append(df_temp)
        except:
            continue
    return pd.concat(total_df, ignore_index=True) if total_df else pd.DataFrame()

df = carregar_corpus(LISTA_DE_IDS)

# --- INTERFACE DE FILTROS ---
st.divider()
col1, col2 = st.columns([2, 1])

with col1:
    termo = st.text_input("Digite o termo de pesquisa:", placeholder="Ex: am, mente, des")

with col2:
    modo = st.selectbox("Tipo de Filtro:", [
        "Exibir todos os dados disponíveis",
        "Busca por Raiz (Contém)",
        "Busca por Prefixo (Inicia com)",
        "Busca por Sufixo (Termina com)",
        "Palavra Isolada (Exata)",
        "Busca Literal (Respeita maiúsculas/minúsculas)"
    ])

# Identifica a coluna de busca
col = 'Nome' if 'Nome' in df.columns else df.columns[0]

if modo == "Exibir todos os dados disponíveis":
    resultado = df
elif not termo:
    resultado = pd.DataFrame()
else:
    termo = termo.strip()
    if modo == "Busca por Raiz (Contém)":
        resultado = df[df[col].str.contains(termo, case=False, na=False)]
    elif modo == "Busca por Prefixo (Inicia com)":
        resultado = df[df[col].str.startswith(termo, na=False)]
    elif modo == "Busca por Sufixo (Termina com)":
        resultado = df[df[col].str.endswith(termo, na=False)]
    elif modo == "Palavra Isolada (Exata)":
        resultado = df[df[col].astype(str).str.lower() == termo.lower()]
    elif modo == "Busca Literal":
        resultado = df[df[col].str.contains(termo, case=True, na=False)]
    else:
        resultado = pd.DataFrame()

# --- EXIBIÇÃO ---
if not resultado.empty:
    st.subheader(f"📊 Resultados: {len(resultado)} entradas")
    st.dataframe(resultado, use_container_width=True)
    csv = resultado.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar estes resultados (CSV)", csv, "pesquisa.csv", "text/csv")
elif termo:
    st.warning("Nenhum resultado encontrado.")
