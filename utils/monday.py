import toml
import requests

def load_api_key():
    # Carrega as informações do arquivo secrets.toml
    try:
        with open('secrets.toml', 'r') as f:
            secrets = toml.load(f)
            api_key = secrets['monday']['api_key']
            return api_key
    except FileNotFoundError:
        print("Arquivo secrets.toml não encontrado.")
        return None
    except KeyError:
        print("Chave 'api_key' não encontrada no arquivo secrets.toml.")
        return None

# Informações de autenticação para a conexão com a API do Monday.com
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": load_api_key()}

def get_board_info():
    query = '{boards(limit:1) { name id description items { name column_values{title id type text } } } }'
    data = {'query': query}
    response = requests.post(url=apiUrl, json=data, headers=headers)
    return response.json()
