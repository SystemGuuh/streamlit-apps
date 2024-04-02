import streamlit as st
from utils.monday import *
import pandas as pd
from monday import MondayClient


def processDataFromARequest(response_data):
    #pensar numa logica para pegar os dados e colocar em diferentes dataframes
    st.write("Building...")


st.set_page_config(page_title="Plotting Sprint", page_icon="🗂️")
st.markdown("# Connecting to Monday API")

#não pega os dados do monday corretamente
monday = MondayClient(load_api_key())
boardQuery = monday.boards.fetch_boards_by_id(6303323231)


response_data = makeRequestByQuery("""
        query {
            boards (ids: 6303323231) {
                groups {
                    title
                    id
                }
                items_page{
                        items {
                            name 
                        column_values {
                        column {
                            title
                        } 
                        text 
                        } 
                    }
                }
            }
        }
        """)

st.write(response_data)
processDataFromARequest(response_data)