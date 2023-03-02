import requests

response = requests.get('https://oauth2.googleapis.com/token')
data = response.json()
