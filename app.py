import streamlit as st
import pandas as pd
import unicodedata

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Buscador DI - GREMD", layout="wide")

def remover_acentos(texto):
    if not isinstance(texto, str): return str(texto)
    return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# --- CABEÇALHO ---
st.subheader("Busca no Dicionário Informal – Dez/2025")
st.markdown("Permite a busca facilitada nos termos do Dicionário Informal, com dados de dezembro de 2025, e permite que os resultados sejam exportados em forma de planilha.")

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
            df_temp = pd.read_csv(url, on_bad_lines='skip')
            total_df.append(df_temp)
        except: continue
    if not total_df: return pd.DataFrame()
    full_df = pd.concat(total_df, ignore_index=True)
    col_nome = 'Nome' if 'Nome' in full_df.columns else full_df.columns[0]
    full_df['busca_limpa'] = full_df[col_nome].apply(remover_acentos).str.lower()
    return full_df

df = carregar_corpus(LISTA_DE_IDS)

# --- LAYOUT EM COLUNAS ---
col_busca, col_manual = st.columns([1.5, 1])

with col_busca:
    with st.form("meu_form"):
        st.write("**Termo de Busca**")
        termo = st.text_input(label="Termo", label_visibility="collapsed", placeholder="Digite aqui...")
        botao_buscar = st.form_submit_button("🔍 BUSCAR")

with col_manual:
    st.markdown("""
    🔍 **Guia Rápido de Uso** Busca por Raiz: apenas o termo (ex: olhos)  
    Palavra Isolada: .termo. (ex: .de.)  
    Busca por Prefixo: termo+\* (ex: ab+\*)  
    Busca por Sufixo: \*+termo (ex: \*+bessa)  
    Busca Literal: use pontos no lugar dos espaços (ex: .pé.de.moleque.)  
    Resetar: deixe vazio para ver a lista completa (A-Z)
    
    🗳️ **Como Exportar (Planilha)** Depois da sua busca, clique no botão **Baixar CSV** que aparecerá abaixo da tabela.
    """)

# --- LÓGICA DE BUSCA ---
if botao_buscar or termo == "":
    t_raw = termo.strip()
    if t_raw == "":
        resultado = df
    else:
        if t_raw.startswith(".") and t_raw.endswith("."):
            t_limpo = remover_acentos(t_raw.replace(".", "")).lower()
            resultado = df[df['busca_limpa'] == t_limpo]
        elif t_raw.endswith("+*"):
            t_limpo = remover_acentos(t_raw.replace("+*", "")).lower()
            resultado = df[df['busca_limpa'].str.startswith(t_limpo, na=False)]
        elif t_raw.startswith("*+"):
            t_limpo = remover_acentos(t_raw.replace("*+", "")).lower()
            resultado = df[df['busca_limpa'].str.endswith(t_limpo, na=False)]
        else:
            t_limpo = remover_acentos(t_raw).lower()
            resultado = df[df['busca_limpa'].str.contains(t_limpo, na=False)]
else:
    resultado = df

# --- EXIBIÇÃO ---
if not resultado.empty:
    st.success(f"{len(resultado)} resultados encontrados.")
    df_exibir = resultado.drop(columns=['busca_limpa'], errors='ignore')
    st.dataframe(df_exibir, use_container_width=True)
    
    csv = df_exibir.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar CSV", csv, "pesquisa.csv", "text/csv")
else:
    st.error("Nenhum resultado encontrado.")

# --- RODAPÉ ---
st.divider()
st.caption("Os dados referenciados pertencem ao [Dicionário Informal](https://www.dicionarioinformal.com.br/) e os links das planilhas redirecionam para a fonte original.")
st.caption(f"Orientador: Prof. Dr. Vitor Nóbrega (DL-USP) | Amanda Gouveia (amandamg@usp.br) | Evelini Cruz Andrade (evelini.andrade@usp.br)")
