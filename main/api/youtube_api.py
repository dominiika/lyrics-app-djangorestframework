import requests


class YoutubeAPI:
    def __init__(self, key):
        self.key = key

    def get_video_url(self, title, artist):
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "snippet",
            "q": f"{title} {artist}",
            "key": self.key,
            "maxResults": 1,
            "type": "video",
            "videoLicense": "youtube",
        }
        response = requests.get(search_url, params=search_params)
        result_id = response.json()["items"][0]["id"]["videoId"]
        embed_url = f"https://www.youtube.com/embed/{result_id}"
        return embed_url
