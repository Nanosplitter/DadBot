import requests


class SongConverter:
    def convert(self, url):
        url = url.strip()
        response = requests.get(
            "https://api.song.link/v1-alpha.1/links", params={"url": url}
        )

        if response.status_code == 200:
            data = response.json()

            platforms = ["appleMusic", "spotify", "youtube"]
            links = {
                platform: data.get("linksByPlatform", {})
                .get(platform, {})
                .get("url", None)
                for platform in platforms
            }
            title = self.get_first_available_title(data, platforms)

            return Song(title, links["appleMusic"], links["spotify"], links["youtube"])
        else:
            return None

    def get_first_available_title(self, data, platforms):
        for platform in platforms:
            entity_id = (
                data.get("linksByPlatform", {})
                .get(platform, {})
                .get("entityUniqueId", None)
            )
            if entity_id:
                return data["entitiesByUniqueId"].get(entity_id, {}).get("title", None)
        return None


class Song:
    def __init__(self, title, apple_music, spotify, youtube):
        self.title = title
        self.apple_music = apple_music
        self.spotify = spotify
        self.youtube = youtube

    def isValid(self):
        return [self.apple_music, self.spotify, self.youtube].count(None) <= 1
