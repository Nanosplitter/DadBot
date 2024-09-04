import re
import yaml
import nextcord

from services import song_converter


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class MusicDetector:
    def __init__(self):
        pass

    async def detectMusic(self, message):
        if message.guild.id not in [
            856919397754470420,
            850473081063211048,
            408321710568505344,
        ]:
            return

        urls = re.findall("(?P<url>https?://[^\s]+)", message.content)

        if urls is None:
            return

        converter = song_converter.SongConverter()

        for url in urls:
            if "spotify.com" in url or "music.apple.com" in url or "youtube.com" in url:
                song = converter.convert(url)
                if song is not None and song.isValid():
                    try:
                        await message.channel.send(
                            f"Alternate links for {song.title}",
                            view=LinkView(song),
                            suppress_embeds=True,
                        )
                    except:
                        pass


class LinkView(nextcord.ui.View):
    def __init__(self, song):
        super().__init__()
        if song.apple_music is not None:
            self.add_item(nextcord.ui.Button(label="Apple Music", url=song.apple_music))
        if song.spotify is not None:
            self.add_item(nextcord.ui.Button(label="Spotify", url=song.spotify))
        if song.youtube is not None:
            self.add_item(nextcord.ui.Button(label="YouTube", url=song.youtube))
