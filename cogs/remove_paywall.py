import re
import urllib.parse
import nextcord
from nextcord.ext import commands

class RemovePaywall(commands.Cog, name="remove_paywall"):
    def __init__(self, bot):
        self.bot = bot

    def create_link_buttons(self, urls):
        view = nextcord.ui.View()
        for url in urls:
            parsed_url = urllib.parse.urlparse(url)
            domain = parsed_url.netloc.replace('www.', '')
            paywall_removed_link = f"https://removepaywall.com/{url}"
            button = nextcord.ui.Button(label=domain, url=paywall_removed_link)
            view.add_item(button)
        return view

    @nextcord.message_command(name="remove paywall")
    async def remove_paywall(self, interaction: nextcord.Interaction, message: nextcord.Message):
        """
        Remove paywall from a message
        """
        pattern = r'(https?://\S+)'
        urls = re.findall(pattern, message.content)
        if urls:
            view = self.create_link_buttons(urls)
            await interaction.response.send_message("", view=view)
        else:
            await interaction.response.send_message("No link found in the message.", ephemeral=True)

def setup(bot):
    bot.add_cog(RemovePaywall(bot))
