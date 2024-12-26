import re
import yaml
import nextcord

from cogs.remove_paywall import RemovePaywall

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
    
    enabled_guild_ids = [
        856919397754470420,
        850473081063211048,
        408321710568505344,
        940645588205187133,
        693254450055348294
    ]

    async def detectPaywall(self, message):
        if message.guild and message.guild.id not in self.enabled_guild_ids:
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
                "It looks like a link in that message may contain a paywall - here's my attempt to remove it:",
                view=view
            )
