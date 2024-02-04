from googleapiclient.discovery import build
import os
import isodate

class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key = os.getenv('YT_API_KEY')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале"""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(channel)

    # FORMATTED
    # def print_info(self) -> None:
    #     """Выводит в консоль информацию о канале"""
    #     request = self.youtube.channels().list(
    #         id=self.channel_id,
    #         part='snippet,statistics'
    #     )
    #     response = request.execute()

        # if response.get('items'):
        #     channel_info = response['items'][0]
        #     snippet = channel_info['snippet']
        #     statistics = channel_info['statistics']
        #     print(f"Название канала: {snippet.get('title')}")
        #     print(f"Описание: {snippet.get('description')}")
        #     print(f"Количество подписчиков: {statistics.get('subscriberCount')}")
        #     print(f"Количество видео: {statistics.get('videoCount')}")
        #     print(f"Количество просмотров: {statistics.get('viewCount')}")
        # else:
        #     print("Информация о канале не найдена.")
