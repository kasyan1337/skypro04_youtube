from src.channel import Channel
class Video:

    def __init__(self, video_id):
        self.video_id = video_id

        self.video_name = ''
        self.video_url = ''
        self.video_views = 0
        self.video_likes = 0
        self.get_video_details()

    def get_video_details(self):
        youtube = Channel.get_service()

        video_response = youtube.videos().list(
            part='snippet,statistics',
            id=self.video_id
        ).execute()

        if video_response['items']:
            video_data = video_response['items'][0]
            self.video_name = video_data['snippet']['title']
            self.video_url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.video_views = video_data['statistics'].get('viewCount', 0)
            self.video_likes = video_data['statistics'].get('likeCount', 0)
        else:
            self.video_name = ''
            self.video_url = ''
            self.video_views = 0
            self.video_likes = 0

    def __str__(self):
        return self.video_name


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.playlist_id = playlist_id

