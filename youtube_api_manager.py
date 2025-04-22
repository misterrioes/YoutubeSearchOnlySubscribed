from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import json
import os
from typing import List, Dict, Any

class YouTubeAPIManager:
    def __init__(self, api_key: str):
        """
        Initialize the YouTube API manager with an API key.
        
        Args:
            api_key (str): Your YouTube Data API v3 key
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        
    def get_channel_subscriptions(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get all subscriptions for a given channel ID.
        
        Args:
            channel_id (str): The YouTube channel ID to get subscriptions for
            max_results (int): Maximum number of results per page (default: 50)
            
        Returns:
            List[Dict[str, Any]]: List of subscription items
        """
        all_subscriptions = []
        next_page_token = None
        
        try:
            while True:
                request = self.youtube.subscriptions().list(
                    part='snippet,contentDetails',
                    channelId=channel_id,
                    maxResults=max_results,
                    pageToken=next_page_token
                )
                response = request.execute()
                
                all_subscriptions.extend(response['items'])
                
                next_page_token = response.get('nextPageToken')
                if not next_page_token:
                    break
                    
            return all_subscriptions
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
            
    def get_upload_playlist_ids(self, subscriptions: List[Dict[str, Any]]) -> List[str]:
        """
        Get the upload playlist IDs for a list of channel subscriptions.
        
        Args:
            subscriptions (List[Dict[str, Any]]): List of subscription items
            
        Returns:
            List[str]: List of upload playlist IDs
        """
        upload_playlist_ids = []
        
        try:
            for subscription in subscriptions:
                channel_id = subscription['snippet']['resourceId']['channelId']
                request = self.youtube.channels().list(
                    part='contentDetails',
                    id=channel_id
                )
                response = request.execute()
                
                if response['items']:
                    upload_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                    upload_playlist_ids.append(upload_playlist_id)
                    
            return upload_playlist_ids
            
        except HttpError as e:
            print(f"An HTTP error occurred: {e}")
            return []
            
    def save_to_file(self, data: Any, filename: str) -> None:
        """
        Save data to a JSON file.
        
        Args:
            data (Any): Data to save
            filename (str): Name of the file to save to
        """
        try:
            if os.path.exists(filename):
                os.remove(filename)
                
            with open(filename, 'w') as f:
                json.dump(data, f, indent=4, sort_keys=True)
                
        except IOError as e:
            print(f"An error occurred while saving to file: {e}")

def main():
    # Replace with your API key
    API_KEY = 'YOUR_API_KEY'
    CHANNEL_ID = 'UCn3bePAgpf2LnV2jN3i5yew'  # Replace with your channel ID
    
    # Initialize the YouTube API manager
    youtube_manager = YouTubeAPIManager(API_KEY)
    
    # Get all subscriptions
    print("Fetching channel subscriptions...")
    subscriptions = youtube_manager.get_channel_subscriptions(CHANNEL_ID)
    
    if subscriptions:
        # Save subscriptions to file
        youtube_manager.save_to_file(subscriptions, 'allMyYoutubeSubscriptions.txt')
        print(f"Saved {len(subscriptions)} subscriptions to file")
        
        # Get upload playlist IDs
        print("Fetching upload playlist IDs...")
        upload_playlist_ids = youtube_manager.get_upload_playlist_ids(subscriptions)
        
        if upload_playlist_ids:
            # Save upload playlist IDs to file
            youtube_manager.save_to_file(upload_playlist_ids, 'allMyYoutubeSubscriptionsUploadedVideosPlaylistIds.txt')
            print(f"Saved {len(upload_playlist_ids)} upload playlist IDs to file")
            
            # Create comma-separated string of playlist IDs
            playlist_ids_str = ','.join(upload_playlist_ids)
            print("Comma-separated playlist IDs:", playlist_ids_str)
            
if __name__ == "__main__":
    main()