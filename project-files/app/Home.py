import streamlit as st
from components import brand

# Colocar a marca no topo
brand.put()

# Definir título da página principal
st.title("Bem-vindo à Aplicação!")

# Descrição introdutória
st.write("Selecione uma das opções abaixo para navegar diretamente pelas diferentes páginas do aplicativo.")

# Dividindo a página em colunas para criar os "cards" das opções
col1, col2, col3 = st.columns(3)

# Card 1: Link direto para a página de Similaridade de Produtos
with col1:
    st.header("Similaridade de Produtos")
    st.write("Encontre os produtos mais similares usando inteligência artificial.")
    st.markdown("[Ir para Similaridade de Produtos](./Similaridade)")

# Card 2: Link direto para a página de Criação de Anúncio
with col2:
    st.header("Criar Anúncio")
    st.write("Crie um anúncio para seus produtos e gere imagens usando IA.")
    st.markdown("[Ir para Criar Anúncio](./Criar)")

# Card 3: Link direto para a página de Dashboard
with col3:
    st.header("Dashboard")
    st.write("Visualize dados e métricas no painel de controle.")
    st.markdown("[Ir para o Dashboard](./Dashboard)")
