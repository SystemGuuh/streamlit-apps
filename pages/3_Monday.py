import requests
import streamlit as st
from utils.monday import *

st.set_page_config(page_title="Plotting Sprint", page_icon="🗂️")
st.markdown("# Connecting to Monday API")



r = get_board_info()
print(r)