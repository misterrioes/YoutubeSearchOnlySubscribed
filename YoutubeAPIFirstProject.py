from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os

# YouTube API configuration
apiKey = 'AIzaSyAc09Rky8SxgTihvTCyMOoOBICnXNWJ0po'
channelId = 'UCn3bePAgpf2LnV2jN3i5yew'

try:
    # Initialize YouTube API client
    youtube = build('youtube', 'v3', developerKey=apiKey)
    
    # First request to get content details
    request = youtube.subscriptions().list(
        part='contentDetails',
        channelId=channelId,
        maxResults=50
    )
    response = request.execute()
    
    # Store all subscription items
    allMySubcriptionItems = []
    for channelInformation in response['items']:
        allMySubcriptionItems.append(channelInformation)
    
    # Second request to get snippet information
    request = youtube.subscriptions().list(
        part='snippet',
        channelId=channelId,
        maxResults=50,
        pageToken=response["nextPageToken"]
    )
    response = request.execute()
    
    # Process each subscription to get upload playlist IDs
    UploadedPlayListItemIds = []
    for channelInformation in response['items']:
        allMySubcriptionItems.append(channelInformation)
        
        # Get channel details to find upload playlist ID
        request = youtube.channels().list(
            part='contentDetails',
            maxResults=1,
            id=channelInformation['snippet']['resourceId']['channelId']
        )
        response = request.execute()
        
        if response['items']:
            upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
            UploadedPlayListItemIds.append(upload_playlist_id)
            print(f"Found upload playlist ID: {upload_playlist_id}")
    
    # Create comma-separated string of all playlist IDs
    first = True
    allPlaylistIdsCommaSeparated = ''
    for playlist_id in UploadedPlayListItemIds:
        if first:
            allPlaylistIdsCommaSeparated = playlist_id
            first = False
        else:
            allPlaylistIdsCommaSeparated = allPlaylistIdsCommaSeparated + ',' + playlist_id
    
    print("All playlist IDs (comma-separated):", allPlaylistIdsCommaSeparated)
    
    # Save subscription data to file
    if os.path.exists("allMyYoutubeSubscriptionsContentDetails.txt"):
        os.remove("allMyYoutubeSubscriptionsContentDetails.txt")
    
    with open("allMyYoutubeSubscriptionsContentDetails.txt", "w") as f:
        json.dump(allMySubcriptionItems, f, sort_keys=True, indent=4)
    
    print("Successfully saved subscription data to file")

except HttpError as e:
    print(f"An error occurred: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

