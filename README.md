# Busca no Dicionário Informal – Dez/2025

Interface interativa desenvolvida para o **GREMD-USP** (Grupo de Estudos em Morfologia Distribuída) com o objetivo de facilitar a coleta e análise morfológica de termos extraídos do Dicionário Informal.

## 🚀 Migração Técnica
Este projeto foi originalmente concebido no **Looker Studio**, mas migrou para uma aplicação personalizada em **Streamlit** para permitir buscas morfológicas complexas via **Expressões Regulares (Regex)** e automação de filtros por símbolos.

## 🛠️ Stack Técnica
- **Linguagem:** Python 3.x
- **Bibliotecas:** Pandas (Tratamento de dados), Streamlit (Interface), Re (Busca avançada).
- **Infraestrutura:** GitHub (Versionamento) e Streamlit Cloud (Hospedagem).

## 🔍 Manual de Busca Automática
O sistema identifica o tipo de pesquisa através de símbolos inseridos no campo de texto:
- `olhos`: Busca por **Raiz** (contém o termo).
- `des+*`: Busca por **Prefixo** (começa com o termo).
- `*+mente`: Busca por **Sufixo** (termina com o termo).
- `.de.`: Busca por **Palavra Isolada** (ignora fragmentos internos).

## 👥 Créditos e Orientação
- **Orientador:** Prof. Dr. Vitor Nóbrega (DL-USP)
- **Extração de Dados:** Amanda Gouveia
- **Modelagem e Interface:** Evelini Cruz Andrade

---
*Dados referenciados pertencem ao [Dicionário Informal](https://www.dicionarioinformal.com.br/).*
