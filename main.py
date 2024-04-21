import requests
from googleapiclient.discovery import build
from env import sec
import json
api_key = sec
youtube = build('youtube', 'v3', developerKey=api_key)


response = requests.get(f'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&key={api_key}')

if response.status_code == 200:

    with open('test.json', 'w') as f:
        json.dump(response.json(), f, indent=4)



