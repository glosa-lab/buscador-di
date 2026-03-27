import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Buscador DI", layout="wide")
st.title("📖 Buscador do Dicionário Informal")

# ID da sua pasta do Google Drive
FOLDER_ID = "18zIHyS5sGaflDAIG9gongF6wm8JiKdt5"

@st.cache_data(ttl=3600) # Atualiza a cada 1 hora
def carregar_todos_os_dados(folder_id):
    # Link para listar os arquivos da pasta (formato exportação)
    # Nota: Como são muitas planilhas, o ideal é que elas estejam como "Qualquer pessoa com o link"
    
    # Lista para armazenar os caminhos das planilhas que o Python vai ler
    # Para simplificar agora, vamos usar a lógica de exportação direta do Google
    # Substituiremos pelos IDs reais se houver erro de permissão
    st.info("Carregando corpus... Isso pode levar alguns segundos devido ao volume de dados.")
    
    # Aqui o ideal seria listar via API, mas para manter CUSTO ZERO e SIMPLICIDADE:
    # Vamos focar na busca dentro do dataframe consolidado.
    # Por enquanto, adicione os IDs das planilhas mais importantes abaixo para teste:
    ids_test = ["ID_DA_PLANILHA_1", "ID_DA_PLANILHA_2"] 
    
    total_dados = []
    for sheet_id in ids_test:
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        try:
            df = pd.read_csv(url)
            total_dados.append(df)
        except:
            continue
    
    return pd.concat(total_dados, ignore_index=True) if total_dados else pd.DataFrame()

# --- INTERFACE DE BUSCA ---
busca = st.text_input("Digite o que procura (raiz, prefixo ou sufixo):")

# Dica para o usuário (baseado no seu guia)
st.caption("Dica: Use 'palavra$' para sufixos ou '^palavra' para prefixos.")

# Se você já tiver uma planilha mestre ou quiser que eu ajude a gerar a lista de IDs:
# Me avise, pois o Python precisa dos IDs individuais de cada uma das 30 planilhas.
