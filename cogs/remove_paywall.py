import re
import nextcord
from nextcord.ext import commands

class RemovePaywall(commands.Cog, name="remove_paywall"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.message_command(name="remove paywall")
    async def remove_paywall(self, interaction: nextcord.Interaction, message: nextcord.Message):
        pattern = r'(https?://\S+)'
        match = re.search(pattern, message.content)
        if match:
            link = match.group(0)
            paywall_removed_link = f"https://removepaywall.com/{link}"

            button = nextcord.ui.Button(label="Open Paywall-Removed Link", url=paywall_removed_link)
            view = nextcord.ui.View()
            view.add_item(button)

            await interaction.response.send_message("", view=view)
        else:
            await interaction.response.send_message("No link found in the message.", ephemeral=True)

def setup(bot):
    bot.add_cog(RemovePaywall(bot))
