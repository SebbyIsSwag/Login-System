import requests

response = requests.get('binaryauthorization.googleapis.com
    client_id=<YOUR_CLIENT_ID>&
    redirect_uri=<YOUR_REDIRECT_URI>&
    response_type=code&
    scope=https://www.googleapis.com/auth/drive&
    access_type=offline')
data = response.json()
