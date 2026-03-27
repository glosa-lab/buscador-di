import streamlit as st
import pandas as pd
import unicodedata
import re

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
            # Limpa nomes de colunas (remove espaços extras que podem vir da planilha)
            df_temp.columns = df_temp.columns.str.strip()
            total_df.append(df_temp)
        except: continue
    
    if not total_df: return pd.DataFrame()
    full_df = pd.concat(total_df, ignore_index=True)
    
    # Padronização da coluna de Nome
    col_nome = 'Nome' if 'Nome' in full_df.columns else full_df.columns[0]
    full_df = full_df.rename(columns={col_nome: 'Nome'})
    
    # Tratamento rigoroso da coluna de Links
    if 'Link' in full_df.columns:
        full_df = full_df.rename(columns={'Link': 'Links'})
    
    # Se a coluna 'Links' ainda estiver vazia ou não existir, gera o link pelo Nome
    if 'Links' not in full_df.columns:
        full_df['Links'] = ""
        
    full_df['Links'] = full_df.apply(
        lambda row: row['Links'] if pd.notna(row['Links']) and str(row['Links']).startswith('http') 
        else f"https://www.dicionarioinformal.com.br/{str(row['Nome']).replace(' ', '-')}/", 
        axis=1
    )
    
    # Data de Acesso
    full_df['Data de Acesso'] = "Dezembro/2025"
    
    # Busca morfológica
    full_df['busca_limpa'] = full_df['Nome'].apply(remover_acentos).str.lower()
    
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
    
    🗳️ **Exportação:** CSV configurado para Excel (separador ';').
    """)

# --- LÓGICA DE BUSCA ---
if botao_buscar or termo == "":
    t_raw = termo.strip()
    if t_raw == "":
        resultado = df
    else:
        if t_raw.startswith(".") and t_raw.endswith("."):
            t_limpo = remover_acentos(t_raw.replace(".", "")).lower()
            padrao = rf"\b{re.escape(t_limpo)}\b"
            resultado = df[df['busca_limpa'].str.contains(padrao, regex=True, na=False)]
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

# --- EXIBIÇÃO E EXPORTAÇÃO ---
if not resultado.empty:
    st.success(f"{len(resultado)} resultados encontrados.")
    
    colunas_finais = ['Nome', 'Links', 'Data de Acesso']
    df_exibir = resultado[colunas_finais]
    
    st.dataframe(df_exibir, use_container_width=True)
    
    # Exportação com separador ';' e encoding para Excel
    csv = df_exibir.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 Baixar Planilha", csv, "dados_morfologia.csv", "text/csv")
else:
    st.error("Nenhum resultado encontrado.")

# --- RODAPÉ ---
st.divider()
st.caption("Os dados referenciados pertencem ao [Dicionário Informal](https://www.dicionarioinformal.com.br/) e os links das planilhas redirecionam para a fonte original.")
st.caption(f"Orientador: Prof. Dr. Vitor Nóbrega (DL-USP) | Desenvolvido por: Amanda Gouveia (amandamg@usp.br) | Evelini Cruz Andrade (evelini.andrade@usp.br)")
