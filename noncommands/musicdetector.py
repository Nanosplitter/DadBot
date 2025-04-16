import re
import yaml
import nextcord

from services import song_converter

from noncommands.constants import SETTINGS_HINT


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class MusicDetector:
    def __init__(self):
        pass

    async def detectMusic(self, message, settings):        
        if not settings.get("music_detector_enabled") == "True":
            return

        urls = re.findall("(?P<url>https?://[^\s]+)", message.content)

        if urls is None:
            return

        converter = song_converter.SongConverter()

        for url in urls:
            song = converter.convert(url)
            if song is not None and song.isValid():
                try:
                    await message.channel.send(
                        f"Alternate links for {song.title}\n{SETTINGS_HINT}",
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
        
        delete_button = nextcord.ui.Button(label="Delete this message", style=nextcord.ButtonStyle.danger)

        async def delete_callback(interaction: nextcord.Interaction):
            await interaction.message.delete()
        
        delete_button.callback = delete_callback
        self.add_item(delete_button)
