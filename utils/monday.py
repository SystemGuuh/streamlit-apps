import toml
import requests
import streamlit as st

def load_api_key():
    return st.secrets['monday']['api_key']

def getBoardResponse():
    headers = {"Authorization": load_api_key()} 
    apiUrl = "https://api.monday.com/v2"
    query = '{boards {name id} }'
    data = {'query': query}
    response = requests.get(url=apiUrl, json=data, headers=headers)
    return response.json()

def getBoardData():
    headers = {"Authorization": load_api_key()} 
    apiUrl = "https://api.monday.com/v2"
    query2 = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
    data = {'query' : query2}

    r = requests.post(url=apiUrl, json=data, headers=headers)
    return r.json()

def makeRequestByQuery(query):
    headers = {"Authorization": load_api_key()} 
    query3 = query
    apiUrl = "https://api.monday.com/v2"
    data = {'query' : query3}
    r = requests.post(url=apiUrl, json=data, headers=headers)
    return r.json()
