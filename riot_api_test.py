import os
import requests
import dotenv

dotenv.load_dotenv()

name = os.getenv('GAME_NAME')
tag = os.getenv('GAME_TAG')
puuid = os.getenv('PUUID')
act_id_5 = '5adc33fa-4f30-2899-f131-6fba64c5dd3a'
act_id_6 = '4c4b8cff-43eb-13d3-8f14-96b783c90cd2'

url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
full_url = url + '?api_key=' + os.getenv('RIOT_API_TOKEN')

match_url = f"https://ap.api.riotgames.com/val/ranked/v1/leaderboards/by-act/{act_id_6}" + '?api_key=' + os.getenv('RIOT_API_TOKEN')
content_url = f"https://ap.api.riotgames.com/val/content/v1/contents" + '?api_key=' + os.getenv('RIOT_API_TOKEN')

res = requests.get(match_url)

# HTTP Status Code
print(res)

print(res.json())
