from datetime import timedelta

import isodate

from src.channel import Channel


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'

        self.get_playlist_details()

    def get_playlist_details(self):
        youtube = Channel.get_service()

        request = youtube.playlists().list(
            id=self.playlist_id,
            part='snippet')

        response = request.execute()

        if response['items']:
            playlist_info = response['items'][0]
            self.title = playlist_info['snippet']['title']
        else:
            self.title = 'Unknown Playlist'
            self.url = ''

    @property
    def total_duration(self):
        """
          - `total_duration` возвращает объект класса `datetime.timedelta`
          с суммарной длительность плейлиста (обращение как к свойству, использовать `@property`)
        """
        youtube = Channel.get_service()

        # Fetch playlist videos
        playlist_videos_response = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos_response['items']]

        # Fetch videos' details
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='contentDetails'  # fetch from content details
        ).execute()

        # SUM OF PLAYLIST DURATION
        total_seconds = sum(isodate.parse_duration(video['contentDetails']['duration']).total_seconds() for video in
                            videos_response['items'])
        return timedelta(seconds=int(total_seconds))

    def show_best_video(self):
        """
          - `show_best_video()` возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков)
        """
        youtube = Channel.get_service()

        # Fetch playlist videos
        playlist_videos_response = youtube.playlistItems().list(
            playlistId=self.playlist_id,
            part='contentDetails',
            maxResults=50
        ).execute()

        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos_response['items']]

        # Fetch videos' details
        videos_response = youtube.videos().list(
            id=','.join(video_ids),
            part='statistics'  # fetching from stats
        ).execute()

        # FIND MOST LIKED VIDEO
        most_liked_video = max(videos_response['items'], key=lambda x: int(x['statistics']['likeCount']))
        most_liked_video_id = most_liked_video['id']

        return f'https://youtu.be/{most_liked_video_id}'
