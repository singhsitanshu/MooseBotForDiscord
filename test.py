import youtube_dl
import os
import requests

query = "trademark usa"
youtube_key = ""

response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&type=video&key={youtube_key}")
format = response.json()

print(format['items'][0]['id']['videoId'])
