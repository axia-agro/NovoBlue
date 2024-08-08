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
    return result

# Interface do Streamlit
def main():
    st.title("Busca de Produtos")
    st.markdown("** CASA DA LAVOURA e SUPREMAX **")
    
    # Definir o caminho fixo da planilha
    file_path = 'Arquivos/De para - Blue 2.0.xlsx'
    
    # Carregar dados
    df = load_data(file_path)
    
    if not df.empty:
        st.write("Dados carregados com sucesso!")
        
        # Campo de busca
        query = st.text_input("Buscar por Código ou Descrição do Produto").strip()
        
        # Inserir uma linha de texto
        st.markdown("### Digite o código ou a descrição ANTIGA do produto na caixa de texto acima.")
        st.markdown("#### Os resultados do NOVO Código e Descrição aparecerão abaixo.")
        
        if query:
            results = search_data(df, query)
            if not results.empty:
                st.write("Resultados encontrados:")
                st.dataframe(results)
            else:
                st.write("Nenhum resultado encontrado.")
    else:
        st.write("Nenhum dado disponível para exibir.")
    
if __name__ == "__main__":
    main()