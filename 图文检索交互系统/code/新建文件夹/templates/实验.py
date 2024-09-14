import requests

url = 'http://localhost:63342/withdraw'
data = {
    'amount': 1000,
    'account': '123456789',
}
response = requests.post(url, data=data)
print(response.text)
