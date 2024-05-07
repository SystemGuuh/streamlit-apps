import streamlit as st
from utils.user import login

def show_main_page():
    st.markdown("""
        Select an option:
        - Sprint Metrics: upload .csv files to analise the a sprint data, files can be generated in our [Scrum Data Dheet](https://docs.google.com/spreadsheets/d/1QHdAKnDqC_1pfwPu89BH1-zxe0Saj8xhqqDfb5nl10Y/edit?usp=sharing)
        - Sprint Data: upload .csv files to analise the data from every sprint, files can be generated in our [Scrum Data Dheet](https://docs.google.com/spreadsheets/d/1QHdAKnDqC_1pfwPu89BH1-zxe0Saj8xhqqDfb5nl10Y/edit?usp=sharing)
        - Database: page connected to our database, its possible to run querys and analise data
        - Monday: page to see data colected from monday API(flow de radar)
    """)

def handle_login(userName, password):
    if login(userName, password):
        st.session_state['loggedIn'] = True
    else:
        st.session_state['loggedIn'] = False
        st.error("Invalid user name or password")

def show_login_page():
    st.write("# Sprints and Database data!")
    userName = st.text_input(label="", value="", placeholder="Enter your user name")
    password = st.text_input(label="", value="", placeholder="Enter password", type="password")
    st.button("Login", on_click=handle_login, args=(userName, password))

def hide_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def show_sidebar():
    st.markdown("""
    <style>
        section[data-testid="stSidebar"][aria-expanded="true"]{
            display: true;
        }
    </style>
    """, unsafe_allow_html=True)

def main():
    hide_sidebar()
    if 'loggedIn' not in st.session_state:
        st.session_state['loggedIn'] = False

    if not st.session_state['loggedIn']:
        show_login_page()
    else:
        show_sidebar()
        show_main_page()

if __name__ == '__main__':
    main()