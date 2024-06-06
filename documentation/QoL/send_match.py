import requests

login_url = "http://localhost:8080/login.php"
match_url = "http://localhost:8080/match.php"

session = requests.Session()

data = {"username": "moa",
 "password": "moa"}

res = session.post(login_url, data=data)
if "Profile" in res.text:
    print("Login successful")

data = {
    "username" : "moa",
    "age" : 22,
    "gender" : "Male",
    "requested_username" : "habibi",
    "punchline" : "hey",
    "custom_filename" : "asdfasdf/koapkfo/erkgk"
}

res = session.post(match_url, data=data)
print(res.text)