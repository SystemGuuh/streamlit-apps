import streamlit as st
from utils.queries import *

def connect():
    # Initialize connection.
    conn = st.connection('mysql', type='sql')
    return conn

def consultBarChart(consulta, conn):
    df = conn.query(consulta, ttl=0)
    column_name = df.columns.tolist()
    st.bar_chart(df, x=str(column_name[0]), y=str(column_name[1]))


def consultArtistas(conn):

    st.write("Quantidade de projetos por estilo musical:")
    consultBarChart(GET_ESTILOS_POR_PROJETO, conn)

    st.write("Quantidade de usuários por UF:")
    consultBarChart(GET_USER_POR_LOCAL, conn)

    #Artistas por local
    #Artistas novos ao longo dos meses
    #Cache médio de artistas por local
    #Shows por local

    ## CONTRATANTES
    #Contratos pela plataforma por contratante
    #Contratante por local
    #Estilo mais contratado
    #Novos contratantes por mes
    #Cache médio de contratante por regiao
    #Contratos por região

def consultContratantes(conn):
    st.write("amora")


st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")

with st.sidebar:
    sprint_selected = st.selectbox("Ver dados:", ['Artistas','Contratantes'])

if sprint_selected == 'Artistas':
    consultArtistas(connect())
if sprint_selected == 'Contratantes':
    consultContratantes(connect())