import streamlit as st
from utils.queries import *

st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")

# Initialize connection.
conn = st.connection('mysql', type='sql')

# Pensar numa forma de otimizar essa chamada
df = conn.query("SELECT * FROM EPM_FILES_TYPE;", ttl=600)

st.dataframe(df, hide_index=True)