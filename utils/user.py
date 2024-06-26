import requests

def login(userName: str, password: str) -> bool:
    if (userName is None):
        return False

    login_data = {
    "username": userName,
    "password": password,
    "loginSource": 1,
    }

    login = requests.post('https://apps.eshows.com.br/eshows/Security/Login',json=login_data).json()
    
    if "error" in login:
        return False

    else:
        if login['data']['success'] == True:
            return True
        else:
            return False