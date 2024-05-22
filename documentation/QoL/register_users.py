import requests
import random
import string
import secrets
import sys


if len(sys.argv) < 2:
    print("[-] usage: python3 register_users.py #accounts")
    sys.exit(-1)

accounts = int(sys.argv[1])

register_url = 'http://localhost:8080/register.php'

for i in range(accounts):
    username: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))
    password: str = "".join(random.choices(string.ascii_uppercase + string.digits, k=12))

    regsiter_data = {
        'username': username,
        'password': password,
        'confirm_password': password,
        'age': random.randint(18,46),
        "gender": secrets.choice(["Male", "Female", "Other"])
    }

    response = requests.post(register_url, data=regsiter_data)
    if "Registration successful" in response.text:
        print(f"[+] Registered {username} successfully!")

