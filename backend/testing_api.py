import requests
import json



url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2')


response = requests.get(url)


Reddit_api = 'FUmo2syXlV5DH88wAteCyf2G9bPBHw'
reddit_url = 'https://api.reddit.com/r/news/top?limit=100'

headers = {
    'Authorization': Reddit_api,
    'User-Agent': 'Daniyal'

}
response = requests.get(reddit_url, headers=headers)
if response.status_code == 200:
    reddit_data = response.json()
    print("Data fetched successfully, processing posts...")
    for post in reddit_data['data']['children']:
        print(post['data']['title'])
        print(post['data']['url'])
        print(post['data']['thumbnail'])

