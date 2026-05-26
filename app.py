import streamlit as st
import pandas as pd
import unicodedata
import re

# --- CONFIGURAÇÃO DA TELA DO BUSCADOR ---
st.set_page_config(page_title="Busca no Dicionário Informal", layout="wide")

def remover_acentos(texto):
    """
    Função que padroniza o texto: remove acentos e caracteres especiais
    para evitar que buscas por constituintes falhem por distração ortográfica.
    """
    if not isinstance(texto, str): return str(texto)
    return "".join(c for c in unicodedata.normalize('NFD', texto) if unicodedata.category(c) != 'Mn')

# --- CABEÇALHO (ESPELHANDO A TELA EM PRODUÇÃO) ---
st.subheader("Busca no Dicionário Informal – Dez/2025")
st.markdown("Permite a busca facilitada nos termos do Dicionário Informal, com dados de dezembro de 2025, e permite que os resultados sejam exportados em forma de planilha.")

# ==============================================================================
# LEITURA AUTOMATIZADA DOS IDs DAS PLANILHAS (BEST PRACTICE)
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
    
    # Mapeamento estrito das colunas com base no cabeçalho real da planilha
    col_nome = 'Nome' if 'Nome' in full_df.columns else full_df.columns[0]
    full_df = full_df.rename(columns={col_nome: 'Nome'})
    
    # Preserva o singular 'Link' conforme a tabela empírica do laboratório
    if 'Links' in full_df.columns:
        full_df = full_df.rename(columns={'Links': 'Link'})
    elif 'Link' not in full_df.columns:
        full_df['Link'] = ""
        
    if 'Data de Acesso' not in full_df.columns:
        full_df['Data de Acesso'] = "Dezembro/2025"
        
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

# --- APLICAÇÃO LÓGICA DE DUPLA VARREDURA (RIGOR DIACRÍTICO) ---
if botao_buscar or termo == "":
    t_raw = termo.strip()
    if t_raw == "":
        resultado = df
    else:
        # Checa se o usuário utilizou acentos na digitação do termo de busca
        tem_acento = t_raw != remover_acentos(t_raw)
        
        # Se contiver acento, a busca é direcionada para a coluna original (Nome)
        # Se NÃO contiver acento, usa a busca_limpa para manter tolerância a falhas
        if tem_acento:
            coluna_alvo = df['Nome'].str.lower()
            t_busca = t_raw.lower()
        else:
            coluna_alvo = df['busca_limpa']
            t_busca = t_raw.lower()

        # Aplicação dos operadores morfológicos regulados por Regex
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
    
    # Exibe na tabela exatamente o trio de colunas homologado na interface gráfica
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
