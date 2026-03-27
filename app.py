import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Buscador DI", layout="wide")
st.title("📖 Buscador do Dicionário Informal")
st.markdown("Pesquisa morfológica — GREMD-USP (Dados de Dez/2025)")

# --- LISTA REAL DE IDs EXTRAÍDOS DOS SEUS LINKS ---
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

@st.cache_data(ttl=86400) # Mantém os dados por 24h para carregar rápido
def carregar_corpus(ids):
    total_df = []
    progresso = st.progress(0)
    status = st.empty()
    
    for i, sheet_id in enumerate(ids):
        status.text(f"Carregando parte {i+1} de {len(ids)}...")
        # Link para forçar o download como CSV, funciona para Sheets e Excel no Drive
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df_temp = pd.read_csv(url)
            total_df.append(df_temp)
        except Exception as e:
            continue
        progresso.progress((i + 1) / len(ids))
    
    status.empty()
    progresso.empty()
    return pd.concat(total_df, ignore_index=True) if total_df else pd.DataFrame()

# Carregamento dos Dados
df = carregar_corpus(LISTA_DE_IDS)

if not df.empty:
    # Interface de Busca - Layout limpo
    termo = st.text_input("Termo de Busca:", placeholder="Ex: olhos, ^ab, bessa$")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        modo = st.radio("Filtro:", ["Contém", "Prefixo (^)", "Sufixo ($)"], horizontal=True)
    
    # Identifica automaticamente a coluna de palavras (geralmente a primeira ou com nome 'Nome')
    coluna_palavra = 'Nome' if 'Nome' in df.columns else df.columns[0]

    if termo:
        if modo == "Contém":
            mask = df[coluna_palavra].str.contains(termo, case=False, na=False)
        elif modo == "Prefixo (^)":
            mask = df[coluna_palavra].str.startswith(termo, na=False)
        else:
            mask = df[coluna_palavra].str.endswith(termo, na=False)
            
        resultado = df[mask]
        
        st.subheader(f"🔍 {len(resultado)} resultados")
        st.dataframe(resultado, use_container_width=True)
        
        # Botão de Exportar - Exatamente como no seu guia
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar resultados (CSV/Planilha)",
            data=csv,
            file_name=f'busca_di_{termo}.csv',
            mime='text/csv',
        )
else:
    st.error("Erro ao ler os dados. Verifique se as planilhas estão com acesso 'Qualquer pessoa com o link'.")
