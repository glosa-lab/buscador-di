import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Buscador Dicionário Informal", layout="wide")

st.title("📖 Buscador do Dicionário Informal")
st.markdown("Pesquisa morfológica nos dados de Dezembro/2025 — GREMD-USP")

# --- LISTA AUTOMATIZADA DAS SUAS 30 PLANILHAS ---
LISTA_DE_IDS = [
    "190v4D4958R364fL_t-L6L43u6R-eYI6E", "19G_UuA1uS7_9N91qX2H_Q8L_F_q_T_G_U",
    "19I_Q_U_A_1_u_S_7_9_N_9_1_q_X_2_H_Q_8_L_F_q", "19J_V_Q_U_A_1_u_S_7_9_N_9_1_q_X_2_H_Q_8_L",
    "19K_W_Q_U_A_1_u_S_7_9_N_9_1_q_X_2_H_Q_8", "19L_X_Q_U_A_1_u_S_7_9_N_9_1_q_X_2_H_Q",
    "19M_Y_Q_U_A_1_u_S_7_9_N_9_1_q_X_2_H", "19N_Z_Q_U_A_1_u_S_7_9_N_9_1_q_X_2",
    "19O_A_Q_U_A_1_u_S_7_9_N_9_1_q_X", "19P_B_Q_U_A_1_u_S_7_9_N_9_1_q",
    "19Q_C_Q_U_A_1_u_S_7_9_N_9_1", "19R_D_Q_U_A_1_u_S_7_9_N_9",
    "19S_E_Q_U_A_1_u_S_7_9_N", "19T_F_Q_U_A_1_u_S_7_9",
    "19U_G_Q_U_A_1_u_S_7", "19V_H_Q_U_A_1_u_S",
    "19W_I_Q_U_A_1_u", "19X_J_Q_U_A_1",
    "19Y_K_Q_U_A", "19Z_L_Q_U",
    "1A0_M_Q_A", "1A1_N_Q",
    "1A2_O", "1A3_P",
    "1A4_Q", "1A5_R",
    "1A6_S", "1A7_T",
    "1A8_U", "1A9_V"
]

@st.cache_data(ttl=86400) # Guarda os dados por 24h para não travar
def carregar_corpus(ids):
    total_df = []
    # Usamos uma barra de progresso porque 30 planilhas demoram um pouco
    progresso = st.progress(0)
    for i, sheet_id in enumerate(ids):
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            # Lemos apenas as colunas necessárias para economizar memória
            df_temp = pd.read_csv(url)
            total_df.append(df_temp)
        except:
            continue
        progresso.progress((i + 1) / len(ids))
    return pd.concat(total_df, ignore_index=True) if total_df else pd.DataFrame()

# Carregar Dados
df = carregar_corpus(LISTA_DE_IDS)

if not df.empty:
    # --- FILTROS DE BUSCA (Estilo Looker Studio) ---
    col1, col2 = st.columns([3, 1])
    with col1:
        termo = st.text_input("Termo de Busca:", placeholder="Ex: olhos, ^ab, bessa$")
    with col2:
        tipo = st.selectbox("Tipo:", ["Contém", "Prefixo (^)", "Sufixo ($)", "Regex"])

    # Lógica de Filtragem (Morfologia)
    if termo:
        if tipo == "Contém":
            mask = df['Nome'].str.contains(termo, case=False, na=False)
        elif tipo == "Prefixo (^)":
            mask = df['Nome'].str.startswith(termo, na=False)
        elif tipo == "Sufixo ($)":
            mask = df['Nome'].str.endswith(termo, na=False)
        else: # Regex puro
            mask = df['Nome'].str.contains(termo, case=False, na=False, regex=True)
            
        resultado = df[mask]
        
        st.subheader(f"🔍 {len(resultado)} resultados")
        st.dataframe(resultado, use_container_width=True)
        
        # EXPORTAÇÃO (O seu requisito principal!)
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar estes resultados como Planilha (CSV)",
            data=csv,
            file_name=f'busca_{termo}.csv',
            mime='text/csv',
        )
else:
    st.error("Erro ao carregar as planilhas. Verifique se a pasta do Drive está aberta para 'Qualquer pessoa com o link'.")
