import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import RetryError
from urllib3 import Retry
from googleapiclient.discovery import build
from env import sec
import json
api_key = sec
youtube = build('youtube', 'v3', developerKey=api_key)
# url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=50&key={}'.format(api_key)

retry_strategy = Retry(
    total=4,  # Maximum number of retries
    status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
)

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)

top_vids = []
def get_top_vids():
    url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=50&order=viewCount&key={}'.format(
        api_key)

    try:
        item_count = 1
        for i in range(5):

            response = http.get(url)

            if response.status_code == 200:

                data = json.loads(response.content.decode('utf-8'))
                items = data['items']

                for item in items:
                    stats = item['statistics']
                    title = item['snippet']['title']
                    views = None
                    likes = None

                    if 'viewCount' in stats:
                        views = int(stats['viewCount'])
                    if 'likeCount' in stats:
                        likes = int(stats['likeCount'])

                    top_vids.append({'title': title,
                                     'views': views,
                                     'likes': likes})
                    item_count += 1


                try:
                    if data['nextPageToken']:
                        next_page = data['nextPageToken']
                        url = 'https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=US&maxResults=50&order=veiwCount&pageToken={}&key={}'.format(next_page, api_key)

                except KeyError:
                    print('No more pages')
                    break

            else:

                print(response.status_code)

    except RetryError as e:

        print(e, '\nRequest Failed: Too many retries')

    with open(f'top_vids.json', 'w') as f:
        sorted_data = sorted(top_vids, key=lambda x: (x['views'], x['likes']), reverse=True)
        json.dump(sorted_data, f, indent=4)
    return top_vids



#current  = 1366
get_top_vids()
count = 0
for vid in top_vids:
    if top_vids.count(vid) == 1:
        print(vid)


