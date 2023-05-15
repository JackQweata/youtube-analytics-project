import os
import googleapiclient.discovery
import isodate


class Video:
    def __init__(self, video_id):
        self.youtube = self.get_service()
        self.video_id = video_id
        self.duration = None
        self.title = None
        self.view_count = None
        self.like_count = None
        self.url = None
        self.populate_video_info()

    def __str__(self):
        return self.title

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey='AIzaSyDCXiFDMn7aFhBp7Sr9BNwfNOClAoPi-Yk')
        return youtube

    def populate_video_info(self):
        try:
            request = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=self.video_id
            )
            response = request.execute()

            if 'items' in response:
                video = response['items'][0]
                self.title = video['snippet']['title']
                self.view_count = int(video['statistics']['viewCount'])
                self.like_count = int(video['statistics']['likeCount'])
                self.url = f"https://youtu.be/{self.video_id}"
                if video['contentDetails']['duration']:
                    self.duration = isodate.parse_duration(video['contentDetails']['duration'])
            else:
                print('Video not found.')
        except Exception:
            return


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

