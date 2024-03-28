import streamlit as st
from utils.monday import *
import pandas as pd
from monday import MondayClient

st.set_page_config(page_title="Plotting Sprint", page_icon="🗂️")
st.markdown("# Connecting to Monday API")

df = pd.json_normalize(getBoardResponse())

#não pega os dados do monday corretamente
monday = MondayClient(load_api_key())
board_data = monday.boards.fetch_boards_by_id(df['account_id'].iloc[0])
board_df = pd.DataFrame(board_data)
st.write(board_data)