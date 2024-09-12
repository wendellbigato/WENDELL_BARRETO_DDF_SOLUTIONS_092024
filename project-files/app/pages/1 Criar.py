import streamlit as st
import pandas as pd
import openai
import os
import json
import random
from dotenv import load_dotenv
from openai import OpenAI

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv('./.env')
openai_api_key = os.getenv('OPENAI_API_KEY')

# Inicializar o cliente da OpenAI
client = OpenAI(api_key=openai_api_key)

# Verificar se a chave da API foi carregada corretamente
if openai_api_key is None:
    st.error("Chave API do OpenAI não encontrada. Verifique o arquivo .env.")
    st.stop()

# Função para gerar uma imagem com base na descrição do produto usando OpenAI (nova abordagem)
def generate_image(description):
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        # O campo 'data' deve ser acessado corretamente
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        st.error(f"Erro ao gerar a imagem: {e}")
        return None

# Função para gerar um preço fictício
def generate_price():
    return round(random.uniform(10.0, 100.0), 2)

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
st.title("Escolha um Produto para Gerar um Anúncio de Venda")

# Permitir ao usuário selecionar um produto baseado no "product_summary"
product_title = st.selectbox("Selecione um produto", df['product_summary'].dropna().unique())

# Aguardar a confirmação do usuário para gerar o anúncio
if st.button("Gerar Anúncio de Venda"):
    if product_title:
        st.write(f"Gerando anúncio para o produto: **{product_title}**")

        # Gerar imagem para o produto usando OpenAI DALL-E
        image_url = generate_image(product_title)

        # Exibir a imagem gerada ou uma imagem fictícia caso falhe
        if image_url:
            st.image(image_url, caption=product_title, use_column_width=True)
        else:
            st.image("https://via.placeholder.com/150", caption=product_title)

        # Detalhes do produto
        product_details = df[df['product_summary'] == product_title].iloc[0]['features']
        categoria = product_details.get('category', 'N/A')
        material = product_details.get('material', 'N/A')

        # Preço fictício
        preco = generate_price()

        # Exibir o anúncio formatado
        st.markdown(f"""
        ### **Anúncio de Venda**
        
        **Produto**: {product_title}
        
        **Descrição**: {product_details.get('description', 'Produto de alta qualidade, ideal para diversas finalidades.')}
        
        **Categoria**: {categoria}
        
        **Material**: {material}
        
        **Preço**: R$ {preco}
        
        """)
        
        # Adicionar um botão fictício de "Comprar"
        st.button(f"Comprar {product_title} por R$ {preco}")
