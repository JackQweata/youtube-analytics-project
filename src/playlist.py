import datetime
import os
import googleapiclient.discovery

from src.video import Video


class PlayList:
    def __init__(self, playlist_id):
        self.url = None
        self.title = None
        self.playlist_id = playlist_id
        self.youtube = self.get_service()
        self.populate_playlist_info()

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey='AIzaSyDCXiFDMn7aFhBp7Sr9BNwfNOClAoPi-Yk')
        return youtube

    def populate_playlist_info(self):
        request = self.youtube.playlists().list(
            part='snippet',
            id=self.playlist_id
        )
        response = request.execute()

        if 'items' in response:
            playlist = response['items'][0]
            self.title = playlist['snippet']['title']
            self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"
        else:
            print('Playlist not found.')

    def get_videos(self):
        request = self.youtube.playlistItems().list(
            part='snippet',
            playlistId=self.playlist_id,
            maxResults=50
        )
        response = request.execute()

        videos = []
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            video = Video(video_id)
            videos.append(video)

        return videos

    @property
    def total_duration(self):
        videos = self.get_videos()
        total_duration = sum([video.duration for video in videos], datetime.timedelta())
        return total_duration

    def show_best_video(self):
        videos = self.get_videos()
        best_video = max(videos, key=lambda video: video.like_count)
        return best_video.url
