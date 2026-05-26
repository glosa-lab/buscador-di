import streamlit as st
import pandas as pd
import unicodedata
import re

# --- CONFIGURAÇÃO DA TELA DO BUSCADOR ---
st.set_page_config(page_title="Busca no Dicionário Informal", layout="wide")

# --- INJEÇÃO DE CSS PARA NIVELAR A ALTURA DOS CONTAINERS ---
st.markdown(
    """
    <style>
        /* Força as colunas do Streamlit a ocuparem 100% da altura da linha */
        [data-testid="stColumn"] {
            display: flex;
            flex-direction: column;
        }
        /* Força os containers internos com borda a esticarem uniformemente */
        [data-testid="stVerticalBlockBorderContainer"] {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }
    </style>
    """,
    unsafe_allow_html=True
)

def remover_acentos(texto):
    """
    Função que padroniza o texto: remove acentos e caracteres especiais
    para evitar que buscas por constituintes falhem por distração ortográfica.
    """
    if not isinstance(texto, str): return str(texto)
    return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# --- CABEÇALHO ---
st.subheader("Busca no Dicionário Informal – Dez/2025")
st.markdown("Permite a busca facilitada nos termos do Dicionário Informal, com dados de dezembro de 2025, e permite que os resultados sejam exportados em forma de planilha.")

# ==============================================================================
# LEITURA AUTOMATIZADA DOS IDs DAS PLANILHAS
# O código busca o arquivo externo 'ids.txt' no repositório para carregar os dados.
# ==============================================================================
def carregar_lista_ids(caminho_arquivo="ids.txt"):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            return [linha.strip() for linha in f if linha.strip()]
    except FileNotFoundError:
        st.error(f"Erro: O arquivo '{caminho_arquivo}' não foi encontrado no repositório GitHub.")
        return []

LISTA_DE_IDS = carregar_lista_ids()
# ==============================================================================

@st.cache_data(ttl=86400)
def carregar_corpus(ids):
    total_df = []
    for sheet_id in ids:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df_temp = pd.read_csv(url, on_bad_lines='skip')
            df_temp.columns = df_temp.columns.str.strip()
            total_df.append(df_temp)
        except: continue
        
    if not total_df: return pd.DataFrame()
    full_df = pd.concat(total_df, ignore_index=True)
    
    col_nome = 'Nome' if 'Nome' in full_df.columns else full_df.columns[0]
    full_df = full_df.rename(columns={col_nome: 'Nome'})
    
    if 'Links' in full_df.columns:
        full_df = full_df.rename(columns={'Links': 'Link'})
    elif 'Link' not in full_df.columns:
        full_df['Link'] = ""
        
    if 'Data de Acesso' not in full_df.columns:
        full_df['Data de Acesso'] = "Dezembro/2025"
        
    full_df['busca_limpa'] = full_df['Nome'].apply(remover_acentos).str.lower()
    return full_df

df = carregar_corpus(LISTA_DE_IDS)

# --- LAYOUT EM COLUNAS EQUILIBRADAS ---
col_busca, col_manual = st.columns([1.5, 1])

with col_busca:
    with st.container(border=True):
        # Elementos do topo da caixa
        with st.container():
            st.write("**Termo de Busca**")
            termo = st.text_input(label="Termo", label_visibility="collapsed", placeholder="Digite aqui...")
        
        # O botão fica isolado na parte inferior devido ao 'justify-content: space-between' do CSS
        botao_buscar = st.button("🔍 BUSCAR", use_container_width=True)

with col_manual:
    with st.container(border=True):
        st.markdown("""
        🔍 **Guia Rápido de Uso**
        * **Busca por Raiz:** apenas o termo (ex: olhos)  
        * **Palavra Isolada:** .termo. (ex: .de.)  
        * **Busca por Prefixo:** termo+\* (ex: ab+\*)  
        * **Busca por Sufixo:** \*+termo (ex: \*+bessa)  
        * **Busca Literal:** use pontos no lugar dos espaços (ex: .pé.de.moleque.)  
        * **Resetar:** deixe vazio para ver a lista completa (A-Z)  
        
        ⚠️ **Rigor Diacrítico (Acentos):**
        * Digitar **com acento** ativa a busca estrita (ex: `.falará.` isola o futuro e ignora *falara*).  
        * Digitar **sem acento** ativa a busca ampla/tolerante (retorna ambos).  
        
        🗳️ **Exportação:** CSV configurado para Excel (separador ';').
        """)

# --- APLICAÇÃO LÓGICA DE DUPLA VARREDURA (RIGOR DIACRÍTICO) ---
if botao_buscar or termo == "":
    t_raw = termo.strip()
    if t_raw == "":
        resultado = df
    else:
        tem_acento = t_raw != remover_acentos(t_raw)
        
        if tem_acento:
            coluna_alvo = df['Nome'].str.lower()
            t_busca = t_raw.lower()
        else:
            coluna_alvo = df['busca_limpa']
            t_busca = t_raw.lower()

        if t_busca.startswith(".") and t_busca.endswith("."):
            t_termo = t_busca.replace(".", "")
            padrao = rf"\b{re.escape(t_termo)}\b"
            resultado = df[coluna_alvo.str.contains(padrao, regex=True, na=False)]
        elif t_busca.endswith("+*"):
            t_termo = t_busca.replace("+*", "")
            resultado = df[coluna_alvo.str.startswith(t_termo, na=False)]
        elif t_busca.startswith("*+"):
            t_termo = t_busca.replace("*+", "")
            resultado = df[coluna_alvo.str.endswith(t_termo, na=False)]
        else:
            resultado = df[coluna_alvo.str.contains(t_busca, na=False)]
else:
    resultado = df

if not resultado.empty:
    st.success(f"{len(resultado)} resultados encontrados.")
    colunas_finais = ['Nome', 'Link', 'Data de Acesso']
    df_exibir = resultado[colunas_finais]
    st.dataframe(df_exibir, use_container_width=True)
    
    csv = df_exibir.to_csv(index=False, sep=';', encoding='utf-8-sig').encode('utf-8-sig')
    st.download_button("📥 Baixar Planilha", csv, "dados_filtrados.csv", "text/csv")
else:
    st.error("Nenhum resultado encontrado.")

# --- RODAPÉ ACADÊMICO ---
st.divider()
st.caption("Os dados referenciados pertencem ao [Dicionário Informal](https://www.dicionarioinformal.com.br/) e os links das planilhas redirecionam para a fonte original.")
st.caption("Orientador: Prof. Dr. Vitor Nóbrega (DL-USP) | Extração de Dados: Amanda Gouveia | Modelagem e Interface: Evelini Cruz Andrade")
st.caption("Ferramentas: Python, Pandas, Streamlit, GitHub, Streamlit Cloud, Google Sheets.")

st.markdown(
    """
    <div style="text-align: right;">
        <a href="https://github.com/glosa-lab/buscador-di" target="_blank" style="text-decoration: none; color: #555; font-size: 13px; font-weight: bold;">
            📄 Ver documentação técnica e registro de migração (GitHub)
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
