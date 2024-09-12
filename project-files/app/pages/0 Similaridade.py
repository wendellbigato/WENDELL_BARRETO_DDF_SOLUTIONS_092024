import streamlit as st
import pandas as pd
import openai
import os
import json
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.schema import Document

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv('./.env')
openai.api_key = os.getenv('OPENAI_API_KEY')

# Verificar se a chave da API foi carregada corretamente
if openai.api_key is None:
    st.error("Chave API do OpenAI não encontrada. Verifique o arquivo .env.")
    st.stop()

# Função para obter embeddings usando OpenAI
def get_embedding(text):
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)
    return embeddings.embed_query(text)

# Função para calcular a similaridade entre produtos (excluindo o produto selecionado)
def find_similar_products(selected_embedding, products_df, selected_product, n_similar=3):
    # Criar uma lista de documentos (usando "product_summary" como nome do produto)
    docs = []
    for idx, row in products_df.iterrows():
        if isinstance(row['product_summary'], str):
            docs.append(Document(page_content=row['product_summary'], metadata={"id": idx}))

    # Gerar embeddings para todos os produtos
    faiss_index = FAISS.from_documents(docs, OpenAIEmbeddings(openai_api_key=openai.api_key))

    # Encontrar os produtos mais similares
    similar_docs = faiss_index.similarity_search_by_vector(selected_embedding, n_similar + 1)  # Buscar um a mais

    # Filtrar para excluir o produto selecionado
    similar_ids = [doc.metadata['id'] for doc in similar_docs if products_df.iloc[doc.metadata['id']]['product_summary'] != selected_product]

    # Retornar os produtos similares
    return products_df.iloc[similar_ids[:n_similar]]

# Carregar o dataset
data_path = './dataset/linhas_validas_com_features.json'

try:
    df = pd.read_json(data_path, lines=True)
except Exception as e:
    st.error(f"Erro ao carregar o dataset: {e}")
    st.stop()

# Verificar se a coluna "features" existe e processar o campo "product_summary"
if 'features' in df.columns:
    # Processar a coluna 'features' para obter 'product_summary'
    df['features'] = df['features'].apply(lambda x: json.loads(x) if isinstance(x, str) else x)
    df['product_summary'] = df['features'].apply(lambda x: x.get('product_summary') if isinstance(x, dict) else None)

    # Verificar se há valores válidos em 'product_summary'
    if df['product_summary'].dropna().empty:
        st.error("Nenhum produto com 'product_summary' encontrado.")
        st.stop()
else:
    st.error("Coluna 'features' não encontrada no dataset.")
    st.stop()

# Exibir a tabela de produtos e permitir que o usuário escolha um produto
st.title("Escolha um Produto para Encontrar os Mais Similares")

# Permitir ao usuário selecionar um produto baseado no "product_summary"
product_title = st.selectbox("Selecione um produto", df['product_summary'].dropna().unique())

# Gerar embedding para o produto selecionado
if product_title:
    selected_embedding = get_embedding(product_title)

    # Encontrar os três produtos mais similares
    if st.button("Encontrar Produtos Similares"):
        similar_products = find_similar_products(selected_embedding, df, product_title)

        st.write("Produtos mais similares:")

        # Exibir os produtos como "cartões de loja"
        cols = st.columns(3)  # Três colunas para exibir os três produtos

        for i, product in similar_products.iterrows():
            with cols[i % 3]:  # Alternar entre as colunas
                # Exibir o título do produto
                st.subheader(product['product_summary'])

                # Exibir detalhes do produto
                st.write(f"Categoria: {product['features'].get('category', 'N/A')}")
                st.write(f"Material: {product['features'].get('material', 'N/A')}")

                # Exibir uma imagem fictícia (pode ser substituída por uma URL real se houver no dataset)
                st.image("https://via.placeholder.com/150", caption=product['product_summary'])
                
                # Adicionar botão de mais detalhes (pode ser usado para acionar algo específico no futuro)
                st.button(f"Ver mais sobre {product['product_summary']}")
