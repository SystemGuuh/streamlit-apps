import time

import numpy as np

import streamlit as st
import pandas as pd

#pensar numa forma de fazer isso aqui
def plotting_demo(df):
    with st.sidebar:
        sprint_selected = st.selectbox("Sprint cicle:", ['Artistas','Contratantes'])

    df['Sprint'] = df['Sprint'].fillna('')
    df_Points = df.drop(columns=['Sprint Start Date','Estimated Effort','Burndown Speed','Required Burndown Speed','Avarege Cycle Time','Weighted Cycle Time'])
    #artista
    if sprint_selected == 'Artistas':
        df_Points = df_Points[df_Points['Sprint'].str.contains('A')]
    if sprint_selected == 'Contratantes':
        df_Points = df_Points[df_Points['Sprint'].str.contains('C')]

    # Realizando a pivotagem
    df_Points_pivot = df_Points.set_index('Sprint').stack().unstack(0)

    st.dataframe(df_Points_pivot, hide_index=True)

    if sprint_selected == 'Artistas':
        df_Points['Sprint'] = df_Points['Sprint'].str.replace('A','').astype(int)
    if sprint_selected == 'Contratantes':
        df_Points['Sprint'] = df_Points['Sprint'].str.replace('C','').astype(int)
    
    st.line_chart(df_Points, x='Sprint', y=(' Total Story Points','Total Sprint Effort'), color=["#ffcc00", "#ff6600"])


st.set_page_config(page_title="Plotting Sprint", page_icon="📈")
st.markdown("# Plotting Sprint Data")

with st.sidebar:
    st.sidebar.header("Plotting metrics")
    uploaded_file = st.file_uploader("Sprint Metrics")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    plotting_demo(df)