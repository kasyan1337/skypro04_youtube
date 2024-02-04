import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        self.youtube = Channel.get_service()

        request = self.youtube.channels().list(id=self._channel_id, part='snippet,statistics')
        response = request.execute()

        if response.get('items'):
            channel_info = response['items'][0]
            snippet = channel_info['snippet']
            statistics = channel_info['statistics']

            self.title = snippet.get('title')
            self.channel_description = snippet.get('description')
            self.url = f"https://www.youtube.com/channel/{self._channel_id}"
            self.channel_subs = int(statistics.get('subscriberCount'))
            self.video_count = int(statistics.get('videoCount'))
            self.channel_views = int(statistics.get('viewCount'))
        else:
            raise ValueError("Что-то пошло не так")

    def __str__(self):
        """<название_канала> (<ссылка_на_канал>)`"""
        return f'{self.title} ({self.url})'

    # Сложение / вычитание / сравнение идет по количеству подписчиков.
    def __add__(self, other):
        return self.channel_subs + other.channel_subs

    def __sub__(self, other):
        return self.channel_subs - other.channel_subs

    def __eq__(self, other):
        return self.channel_subs == other.channel_subs

    def __lt__(self, other):
        return self.channel_subs < other.channel_subs

    def __le__(self, other):
        return self.channel_subs <= other.channel_subs

    def __gt__(self, other):
        return self.channel_subs > other.channel_subs

    def __ge__(self, other):
        return self.channel_subs >= other.channel_subs

    @property
    def channel_id(self):
        """Protect Channel id so it would not change"""
        return self._channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        channel = self.youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        print(channel)

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        api_key = os.getenv('YT_API_KEY')
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_name="channel_info.json"):
        """Сохраняет информацию о канале в JSON файл"""
        format = {
            'channel_id': self._channel_id,
            'title': self.title,
            'channel_description': self.channel_description,
            'url': self.url,
            'channel_subs': self.channel_subs,
            'video_count': self.video_count,
            'channel_views': self.channel_views
        }

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(format, file, ensure_ascii=False, indent=4)
