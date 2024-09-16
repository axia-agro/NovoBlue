import streamlit as st
import pandas as pd

# Configurar a largura da página
st.set_page_config(layout="wide")

st.write("Configuração da página carregada...")

# Carregar os dados do Excel a partir de um caminho fixo
@st.cache_data
def load_data(file_path):
    try:
        st.write("Carregando dados...")
        data = pd.read_excel(file_path, dtype=str)
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()

# Função de busca
def search_data(df, regional, query):
    query = query.lower()
    words = query.split()

    # Filtrar os resultados pela regional selecionada
    regional_df = df[df['REGIONAL'] == regional]

    # Aplicar a busca para cada palavra na query
    mask = pd.Series(True, index=regional_df.index)
    for word in words:
        mask &= regional_df['COD_PRODUTO'].str.lower().str.contains(word) | \
                regional_df['DSC_PRODUTO'].str.lower().str.contains(word)
    
    result = regional_df[mask][['REGIONAL', 'COD_PRODUTO', 'DSC_PRODUTO', 'NOM_MARCA', 'COD_PROTHEUS', 'DSC_PRODUTO2', 'NOM_MARCA2']]

    # Renomear as colunas para exibição
    result.columns = ['Regional', 'Código Antigo', 'Descrição Antiga', 'Marca', 'Novo Código', 'Nova Descrição', 'Nova Marca']

    return result

# Função para aplicar estilos customizados
def highlight_columns(x):
    color = 'background-color: yellow'
    df = pd.DataFrame('', index=x.index, columns=x.columns)
    df[['Novo Código', 'Nova Descrição']] = color
    return df

# Interface do Streamlit
def main():
    st.write("Iniciando a aplicação...")
    
    st.image("logo.png", width=150)
    st.title("Busca de Produtos")
    st.markdown("** CASA DA LAVOURA e SUPREMAX **")

    file_path = 'Arquivos/De para - Blue 2.0.xlsx'

    with st.spinner('Carregando dados...'):
        df = load_data(file_path)
    
    if not df.empty:
        st.success("Dados carregados com sucesso!")
        
        regional_list = sorted(df['REGIONAL'].drop_duplicates())
        selected_regional = st.selectbox("Selecione a Regional", regional_list)

        query = st.text_input("Buscar por Código ou Descrição do Produto").strip().lower()

        st.markdown("### Digite o código ou a descrição ANTIGA do produto na caixa de texto acima.")
        st.markdown("#### Os resultados do NOVO Código e Descrição aparecerão abaixo.")
        
        if query and selected_regional:
            with st.spinner('Procurando resultados...'):
                results = search_data(df, selected_regional, query)
            if not results.empty:
                st.write("Resultados encontrados:")
                styled_results = results.style.apply(highlight_columns, axis=None)
                st.dataframe(styled_results, use_container_width=True, height=600)  # Aumenta a altura da tabela
            else:
                st.warning("Nenhum resultado encontrado.")
        else:
            st.info("Por favor, selecione uma regional e insira uma consulta.")
    else:
        st.error("Nenhum dado disponível para exibir.")
    
if __name__ == "__main__":
    main()