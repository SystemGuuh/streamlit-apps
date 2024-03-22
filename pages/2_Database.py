from urllib.error import URLError

import altair as alt
import pandas as pd

import streamlit as st
from streamlit.hello.utils import show_code
    


st.set_page_config(page_title="Database", page_icon="📊")
st.markdown("# Analisando dados do banco Eshows")
st.sidebar.header("Database")