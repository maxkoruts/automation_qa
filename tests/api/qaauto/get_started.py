import requests
from settings import settings
body = {
  "email": settings.USER_EMAIL,
  "password": settings.USER_PASS,
  "remember": False
}

url_signin = f"{settings.QA_AUTO_API_URL}/auth/signin"
url_get_current = f"{settings.QA_AUTO_API_URL}/users/current"

session = requests.Session()

# response_signin = requests.post(url=url_signin, json=body)
session.post(url=url_signin, json=body)
# cookie = dict(response_signin.cookies)
# print(cookie)
# session.cookies.clear() #чистимо кукі
response = session.get(url=url_get_current)
print(response.status_code)
print(response.json())