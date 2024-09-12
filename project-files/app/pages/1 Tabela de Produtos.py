import streamlit as st
import pandas as pd
import json

# Load the JSON data from the dataset (usando lines=True)
data_path = 'dataset/linhas_validas_com_features.json'
df = pd.read_json(data_path, lines=True)

# Remove a coluna 'features' da tabela principal para exibição
df_no_features = df.drop(columns=['features'])

# Exibir o título da tabela
st.title("Tabela de Produtos")

# Selecionar uma coluna para aplicar o filtro
filter_column = st.selectbox("Escolha uma coluna para filtrar", df_no_features.columns)

# Obter os valores únicos da coluna selecionada
unique_values = df_no_features[filter_column].unique()

# Adicionar um seletor múltiplo para filtrar os valores da coluna
selected_values = st.multiselect(f"Selecione os valores para filtrar na coluna {filter_column}", unique_values)

# Aplicar o filtro baseado nos valores selecionados
if selected_values:
    df_filtered = df_no_features[df_no_features[filter_column].isin(selected_values)]
else:
    df_filtered = df_no_features  # Se não houver filtro, exibir a tabela completa

# Exibir a tabela filtrada
st.dataframe(df_filtered)

