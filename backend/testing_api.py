import requests
import json



url = ('https://newsapi.org/v2/top-headlines?'
       'country=us&'
       'apiKey=f8b02b9635ed4db4bae7cad2ee599cd2')


response = requests.get(url)
print(response.json())