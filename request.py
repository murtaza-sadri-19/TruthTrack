import requests

url = "http://127.0.0.1:5000/prediction"
for _ in range(100):
    response = requests.post(url, data={"chatInput": "Test headline"})
    print(response.status_code)
