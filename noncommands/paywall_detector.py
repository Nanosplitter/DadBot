import re
import yaml
import nextcord

from cogs.remove_paywall import RemovePaywall
from noncommands.constants import SETTINGS_HINT

URL_PATTERN = re.compile(r'https?://\S+')

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class PaywallDetector:
    paywalled_sites = [
        "nytimes.com",
        "washingtonpost.com",
        "wsj.com",
        "ft.com",
        "economist.com",
        "theatlantic.com",
        "bostonglobe.com",
        "businessinsider.com",
        "wired.com"
    ]
    

    async def detectPaywall(self, message, settings):
        if not settings.get("paywall_detector_enabled") == "True":
            return

        urls = URL_PATTERN.findall(message.content)
        if not urls:
            return

        paywall_urls = [url for url in urls if any(site in url for site in self.paywalled_sites)]
        if paywall_urls:
            view = RemovePaywall(None).create_link_buttons(paywall_urls)
            delete_button = nextcord.ui.Button(label="Delete this message", style=nextcord.ButtonStyle.danger)
            
            async def delete_callback(interaction: nextcord.Interaction):
                await interaction.message.delete()
            
            delete_button.callback = delete_callback
            view.add_item(delete_button)
            await message.channel.send(
                f"It looks like a link in that message may contain a paywall - here's my attempt to remove it:\n{SETTINGS_HINT}",
                view=view
            )
            
