import os
import requests
import dotenv

dotenv.load_dotenv()

name = "MeV2"
tag = "LBK"

url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"

