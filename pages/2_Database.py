import streamlit as st
from utils.queries import *

def connect():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    return conn

def consult(conn):
    # Mostra código tabela e printar resultado query
    st.code(GET_EPM_FILES_TYPE, language='sql')
    df = conn.query(GET_EPM_FILES_TYPE, ttl=0)
    st.dataframe(df, hide_index=True)


st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")

consult(connect())