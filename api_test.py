import requests

print(requests.post("http://192.168.0.14:8080/api/wardrobe/", json={"user_id": 3}).json())
