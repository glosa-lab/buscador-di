import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Buscador DI - GREMD", layout="wide")

# --- CABEÇALHO ---
st.title("📖 Buscador do Dicionário Informal")
st.markdown("Ferramenta de análise morfológica — GREMD-USP (Dados de Dez/2025)")

# --- LISTA DE IDs REAIS ---
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
            # Skip bad lines garante que erros de formatação no CSV não travem o carregamento
            df_temp = pd.read_csv(url, on_bad_lines='skip')
            total_df.append(df_temp)
        except:
            continue
    return pd.concat(total_df, ignore_index=True) if total_df else pd.DataFrame()

df = carregar_corpus(LISTA_DE_IDS)

# --- FORMULÁRIO DE BUSCA ---
st.divider()
with st.form("form_busca"):
    col1, col2 = st.columns([2, 1])
    with col1:
        termo = st.text_input("Termo de pesquisa:", placeholder="Digite aqui...")
    with col2:
        modo = st.selectbox("Filtro:", [
            "Exibir todos os dados",
            "Busca por Raiz (Contém)",
            "Busca por Prefixo",
            "Busca por Sufixo",
            "Palavra Isolada (Exata)",
            "Busca Literal"
        ])
    botao_buscar = st.form_submit_button("🔍 BUSCAR")

if botao_buscar:
    col = 'Nome' if 'Nome' in df.columns else df.columns[0]
    if modo == "Exibir todos os dados":
        resultado = df
    elif not termo:
        st.warning("Insira um termo.")
        resultado = pd.DataFrame()
    else:
        termo = termo.strip()
        if modo == "Busca por Raiz (Contém)":
            resultado = df[df[col].str.contains(termo, case=False, na=False)]
        elif modo == "Busca por Prefixo":
            resultado = df[df[col].str.startswith(termo, na=False)]
        elif modo == "Busca por Sufixo":
            resultado = df[df[col].str.endswith(termo, na=False)]
        elif modo == "Palavra Isolada (Exata)":
            resultado = df[df[col].astype(str).str.lower() == termo.lower()]
        elif modo == "Busca Literal":
            resultado = df[df[col].str.contains(termo, case=True, na=False)]

    if not resultado.empty:
        st.success(f"{len(resultado)} resultados encontrados.")
        st.dataframe(resultado, use_container_width=True)
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Baixar CSV", csv, f"pesquisa.csv", "text/csv")
    elif termo:
        st.error("Sem resultados.")

# --- RODAPÉ ---
st.divider()
st.caption("Os dados referenciados pertencem ao [Dicionário Informal](https://www.dicionarioinformal.com.br/) e os links das planilhas redirecionam para a fonte original.")
st.caption(f"Orientador: Prof. Dr. Vitor Nóbrega | Amanda Gouveia (amandamg@usp.br) | Evelini Cruz Andrade (evelini.andrade@usp.br)")
