import requests

response = requests.get("https://nul-pdi.netlify.app/api/books")
data = response.json()

print(data)