import os
import json
import googleapiclient.discovery


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str):
        self.title = None
        self.video_count = None
        self.url = None
        self.view_count = None
        self.subscriber_count = None
        self.description = None
        self.id = None
        self._channel_id = channel_id
        self.youtube = self.get_service()
        self.populate_channel_info()

    def print_info(self):
        request = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        )
        print(request.execute())

    @property
    def channel_id(self):
        return self._channel_id

    @classmethod
    def get_service(cls):
        api_key = os.getenv('YT_API_KEY')
        youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=api_key)
        return youtube

    def populate_channel_info(self):
        request = self.youtube.channels().list(
            part='snippet,statistics',
            id=self.channel_id
        )
        response = request.execute()

        if 'items' in response:
            channel = response['items'][0]
            self.id = channel['id']
            self.title = channel['snippet']['title']
            self.description = channel['snippet']['description']
            self.url = f"https://www.youtube.com/channel/{self.id}"
            self.subscriber_count = int(channel['statistics']['subscriberCount'])
            self.video_count = int(channel['statistics']['videoCount'])
            self.view_count = int(channel['statistics']['viewCount'])
        else:
            print('Channel not found.')

    def to_json(self, filename):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)

    def __str__(self):
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count + other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __sub__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count - other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __eq__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count == other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __ge__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count >= other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __le__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count <= other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __gt__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count > other.subscriber_count
        raise TypeError("Неподдерживаемый тип")

    def __lt__(self, other):
        if isinstance(other, Channel):
            return self.subscriber_count < other.subscriber_count
        raise TypeError("Неподдерживаемый тип")
