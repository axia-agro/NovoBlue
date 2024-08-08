import streamlit as st
import pandas as pd

# Carregar os dados do Excel a partir de um caminho fixo
@st.cache_data
def load_data(file_path):
    try:
        # Especificar que todas as colunas devem ser carregadas como strings
        data = pd.read_excel(file_path, dtype=str)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Função de busca
def search_data(df, query):
    query = query.lower()
    
    # Encontrar a REGIONAL correspondente ao COD_PRODUTO de entrada
    regional_query = df[df['COD_PRODUTO'].str.lower() == query]['REGIONAL'].values
    
    if len(regional_query) > 0:
        regional = regional_query[0]
        # Filtrar resultados pela REGIONAL correspondente
        mask = (df['REGIONAL'] == regional) & (
            df['COD_PRODUTO'].str.contains(query, case=False, na=False) | 
            df['DSC_PRODUTO'].str.lower().str.contains(query, na=False)
        )
    else:
        # Se não encontrar a REGIONAL, buscar normalmente sem filtro de REGIONAL
        mask = df['COD_PRODUTO'].str.contains(query, case=False, na=False) | df['DSC_PRODUTO'].str.lower().str.contains(query, na=False)
    
    result = df[mask][['REGIONAL', 'COD_PROTHEUS', 'DSC_PRODUTO2', 'NOM_MARCA2']]
    result['COD_PROTHEUS'] = result['COD_PROTHEUS'].str.replace(',', '')

    # Renomear as colunas para efeitos de leitura
    result = result.rename(columns={
        'COD_PROTHEUS': 'NOVO CÓDIGO',
        'DSC_PRODUTO2': 'NOVO DESCRITIVO',
        'NOM_MARCA2': 'MARCA'
    })
    
    return result

# Interface do Streamlit
def main():
    st.set_page_config(page_title="BUSCADOR - CASA DA LAVOURA", page_icon="casadalavoura_logo.png")
    
    st.image("casadalavoura_logo.png", width=200)
    st.title("BUSCADOR - CASA DA LAVOURA")
    
    
    # Definir o caminho fixo da planilha
    file_path = 'Arquivos/De para - Blue 2.0.xlsx'
    
    # Carregar dados
    df = load_data(file_path)
    
    if not df.empty:
        st.write("Insira no campo abaixo:")
        
        # Campo de busca
        st.markdown("### Insira o Código ou a Descrição ANTIGA de um produto para buscar seus NOVOS Códigos e Descritivos.")
        query = st.text_input("").strip()
        
        # Inserir uma linha de texto
        st.markdown("### Veja abaixo os novos códigos e descritivos dos produtos. Atente-se a utilizar o código e a descrição de sua regional.")
        
        if query:
            results = search_data(df, query)
            if not results.empty:
                st.write("Resultados encontrados:")
                st.dataframe(results, hide_index=True)
            else:
                st.write("Nenhum resultado encontrado.")
    else:
        st.write("Nenhum dado disponível para exibir.")
    
if __name__ == "__main__":
    main()