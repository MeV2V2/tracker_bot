import os
import requests
import dotenv

dotenv.load_dotenv()

name = os.getenv('GAME_NAME')
tag = os.getenv('GAME_TAG')

url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
full_url = url + '?api_key=' + os.getenv('RIOT_API_TOKEN')

res = requests.get(full_url)

# HTTP Status Code
print(res)

print(res.json())
