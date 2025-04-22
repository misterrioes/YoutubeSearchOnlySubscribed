from urllib import response
from googleapiclient.discovery import build
import json, os



apiKey = 'AIzaSyAc09Rky8SxgTihvTCyMOoOBICnXNWJ0po'
channelId= 'UCn3bePAgpf2LnV2jN3i5yew'
youtube = build('youtube', 'v3', developerKey=apiKey)

request = youtube.playlistItems().list(
   part= 'contentDetails',
   playlistId='UUTMt7iMWa7jy0fNXIktwyLA'
   )
response = request.execute()
print (response)


first =  True
allPlaylistIdsCommaSeparated =   ''
f = open('allMyYoutubeSubscriptionsUploadedVideosPlaylistIds.txt', 'r')
for line in f:
    if first:
        allPlaylistIdsCommaSeparated = f.readline()
        first = False
    else:
        allPlaylistIdsCommaSeparated = allPlaylistIdsCommaSeparated + ','+f.readline()
#print (allPlaylistIdsCommaSeparated.replace('\n',''))

