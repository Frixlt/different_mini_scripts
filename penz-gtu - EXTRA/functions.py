import requests
from bs4 import BeautifulSoup
from config import final_cnfg

def autorisation(session, username, password, url):
    # получаем токен авторизации
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    logintoken = soup.find('input', {'name': 'logintoken'}).get('value')
    # попытка входа в акаунт
    post_request = session.post(url, {
        'logintoken': logintoken,
        'username': username,
        'password': password,
    })
    # проверка вошли ли мы?
    soup = BeautifulSoup(post_request.text, "html.parser")
    if soup.findAll('div', {'class': 'alert alert-danger', 'role': 'alert'}) == []:
        return (True)
    else:
        return (False)

if __name__ == "__main__":
    session = requests.Session()
    url = final_cnfg["links"]['main_site']
    print(autorisation(session, 's000009649', '50815081m', url))