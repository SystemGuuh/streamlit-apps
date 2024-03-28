import streamlit as st
from utils.monday import *
import pandas as pd
from monday import MondayClient


st.set_page_config(page_title="Plotting Sprint", page_icon="🗂️")
st.markdown("# Connecting to Monday API")

#não pega os dados do monday corretamente
monday = MondayClient(load_api_key())
boardQuery = monday.boards.fetch_boards_by_id(6303323231)

#internal server error 500
df = pd.json_normalize(makeRequestByQuery(boardQuery))
st.dataframe(df)
st.write(makeRequestByQuery(boardQuery))
