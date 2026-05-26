# Buscador de Corpora Morfológicos: Dicionário Informal (Dez/2025)

Interface interativa desenvolvida em ambiente de código aberto com o objetivo de facilitar a investigação, filtragem e descrição morfológica de dados linguísticos do **Português Brasileiro (PB)** extraídos do **Dicionário Informal** (https://www.dicionarioinformal.com.br/).

## 🚀 Migração Técnica
Este projeto foi originalmente concebido no **Looker Studio**, mas migrou para uma aplicação personalizada em **Streamlit** (Python 3.x) para permitir análises granulares complexas. A mudança viabiliza a varredura automática de constituintes mínimos e afixos por meio de Expressões Regulares (**Regex**) e processamento de strings diretamente no navegador de internet, eliminando as limitações de latência e rigidez de filtros das ferramentas de relatórios convencionais.

## 🛠️ Stack Técnica e Infraestrutura
* **Fonte de Dados:** Planilhas do **Google Sheets** (armazenamento estático do corpus consumido via exportação direta em formato CSV).
* **Linguagem Base:** **Python 3.x** (estruturação lógica e processamento de strings).
* **Bibliotecas Principais:** * **Pandas:** Unificação de tabelas, higienização estrita de dados e tratamento de nulos.
  * **Streamlit:** Construção da interface gráfica e renderização visual dos formulários.
  * **Re:** Motor nativo de busca avançada por Expressões Regulares.
* **Hospedagem e Controle:** *GitHub* (versionamento e guarda do código-fonte) e *Streamlit Cloud* (hospedagem pública e publicação automática na web).

## 🔍 Manual de Busca Morfológica
O motor de busca identifica o tipo de constituinte linguístico a ser isolado através de símbolos de controle inseridos pelo pesquisador no campo de texto:
* `olhos` : Busca por **Raiz/Substring** (retorna qualquer ocorrência que contenha a sequência de caracteres).
* `des+*` : Busca por **Prefixo** (isola termos que se iniciam estritamente com o elemento delimitado).
* `*+mente` : Busca por **Sufixo** (isola termos que terminam estritamente com o elemento delimitado).
* `.de.` : Busca por **Palavra Isolada** (utiliza marcadores de borda de palavra para ignorar fragmentos internos em outras cadeias complexas).

## 👥 Créditos e Orientação Original
* **Orientação:** Prof. Dr. Vitor Nóbrega (DL-USP)
* **Extração de Dados:** Amanda Gouveia
* **Modelagem de Dados e Interface:** Evelini Cruz Andrade

## 📄 Licença
Este projeto está licensed sob a **Licença MIT** — permitindo o livre uso, modificação e replicação da ferramenta por outros pesquisadores da comunidade acadêmica de Humanidades Digitais e Linguística, desde que mantidos os créditos originais.

---
*Os dados empíricos referenciados pertencem originalmente ao [Dicionário Informal](https://www.dicionarioinformal.com.br/). A aplicação realiza a consolidação e filtragem das tabelas em sua estrutura nativa (`Nome`, `Link`, `Data de Acesso`) respeitando estritamente a fidelidade do corpus coletado.*
