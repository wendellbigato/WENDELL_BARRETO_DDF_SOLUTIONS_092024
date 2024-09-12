import streamlit as st
import jwt
import time

# Configurações do Metabase
METABASE_SITE_URL = "http://metabase-treinamentos.dadosfera.ai"
METABASE_SECRET_KEY = "318f0f138e84ba9be00f9d535b024a5f96dff0ebc83c92735cff748280d26ab2"

# Gera o token JWT com expiração de 10 minutos
payload = {
  "resource": {"dashboard": 183},
  "params": {},
  "exp": round(time.time()) + (60 * 10)  # 10 minutos de expiração
}

token = jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

# URL do iframe para o dashboard embutido
iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + token + "#bordered=true&titled=true"

# Criar a página do dashboard no Streamlit
st.title("Dashboard")

# Incluir o iframe para exibir o dashboard do Metabase
st.markdown(
    f'<iframe src="{iframeUrl}" width="100%" height="800px" frameborder="0"></iframe>',
    unsafe_allow_html=True
)
