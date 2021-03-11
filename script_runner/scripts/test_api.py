import redis
import requests

key = ''
with open("api_key.txt") as file:
    key = file.read()

headers = {
    "apikey": key
}

params = (
    ("league_id","237"),
)

response = requests.get('https://app.sportdataapi.com/api/v1/soccer/seasons', headers=headers, params=params)
print(response.text)
print(response)

with open("responses.txt", 'a') as file:
    file.write(response.text)