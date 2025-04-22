from urllib import response
from googleapiclient.discovery import build
import json, os

apiKey = 'AIzaSyAc09Rky8SxgTihvTCyMOoOBICnXNWJ0po'
channelId= 'UCn3bePAgpf2LnV2jN3i5yew'
youtube = build('youtube', 'v3', developerKey=apiKey)

allMySubcriptions = ''
with open("allMyYoutubeSubscriptions.txt",'r') as allMySubcriptionsFile:
    allMySubcriptions = json.load(allMySubcriptionsFile)

for i in range(len(allMySubcriptions)):
    request = youtube.search().list(
        part='snippet',
        channelId=allMySubcriptions[i]['snippet']['resourceId']['channelId'],
        maxResults=1,
        type='video',
        q='API'
    )
    response = request.execute()
    print (response)
 #  print(response['items'][0]['id']['videoId'])
