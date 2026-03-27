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

    # --- LÓGICA DE FILTRAGEM ---
    # Identifica a coluna principal (ajuste 'Nome' se for outro o título na planilha)
    col = 'Nome' if 'Nome' in df.columns else df.columns[0]
    
    if modo == "Exibir todos os dados disponíveis":
        resultado = df
    elif not termo:
        st.info("Digite um termo para filtrar ou escolha 'Exibir todos'.")
        resultado = pd.DataFrame()
    else:
        termo = termo.strip()
        
        if modo == "Busca por Raiz (Contém)":
            # Procura a sequência de letras em qualquer lugar, ignorando caixa alta/baixa
            resultado = df[df[col].str.contains(termo, case=False, na=False)]
            
        elif modo == "Busca por Prefixo (Inicia com)":
            # Garante que a palavra começa com as letras digitadas
            resultado = df[df[col].str.startswith(termo, na=False)]
            
        elif modo == "Busca por Sufixo (Termina com)":
            # Garante que a palavra termina com as letras digitadas
            resultado = df[df[col].str.endswith(termo, na=False)]
            
        elif modo == "Palavra Isolada (Exata)":
            # A célula precisa ser exatamente igual ao que foi digitado
            resultado = df[df[col].astype(str).str.lower() == termo.lower()]
            
        elif modo == "Busca Literal":
            # Busca 'Contém', mas diferencia 'A' de 'a' (Rigor técnico)
            resultado = df[df[col].str.contains(termo, case=True, na=False)]

    # --- EXIBIÇÃO ---
    if not resultado.empty:
        st.subheader(f"📊 Resultados: {len(resultado)} entradas")
        st.dataframe(resultado, use_container_width=True)
        
        # Exportação
        csv = resultado.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar estes resultados (CSV)",
            data=csv,
            file_name=f"pesquisa_{termo}_{modo.split()[0]}.csv",
            mime='text/csv',
        )
    elif termo:
        st.warning("Nenhum resultado encontrado para os critérios selecionados.")
