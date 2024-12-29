import nextcord
from nextcord.ext import commands
from models.server_settings import ServerSettings
import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class ServerSettingsCog(commands.Cog, name="server_settings"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="settings", description="Manage server settings.", guild_ids=[850473081063211048])
    async def settings(self, interaction: nextcord.Interaction):
        pass

    @settings.subcommand(name="set", description="Enable or disable specific automated actions.")
    @commands.has_permissions(administrator=True)
    async def set_setting(self, interaction: nextcord.Interaction, setting: str, value: bool):
        server_id = interaction.guild.id
        settings, created = ServerSettings.get_or_create(server_id=server_id)
        setattr(settings, setting, value)
        settings.save()
        self.bot.server_settings[server_id] = settings
        await interaction.response.send_message(f"Setting '{setting}' has been {'enabled' if value else 'disabled'}.")

    @settings.subcommand(name="view", description="View the current server settings.")
    async def view_settings(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        settings = self.bot.server_settings.get(server_id)
        if settings:
            settings_dict = settings.__data__
            settings_str = "\n".join([f"{key}: {value}" for key, value in settings_dict.items() if key != "id" and key != "server_id"])
            await interaction.response.send_message(f"Current settings:\n{settings_str}")
        else:
            await interaction.response.send_message("No settings found for this server.")

    @settings.subcommand(name="reset", description="Reset server settings to default values.")
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        settings, created = ServerSettings.get_or_create(server_id=server_id)
        settings.apod_enabled = True
        settings.paywall_detector_enabled = True
        settings.music_detector_enabled = True
        settings.im_checker_enabled = True
        settings.haiku_detector_enabled = True
        settings.save()
        self.bot.server_settings[server_id] = settings
        await interaction.response.send_message("Server settings have been reset to default values.")

    @settings.subcommand(name="autocomplete", description="Autocomplete options for settings.")
    async def autocomplete_settings(self, interaction: nextcord.Interaction, setting: str):
        settings_options = list(config["server_settings"].keys())
        matching_options = [option for option in settings_options if setting.lower() in option.lower()]
        await interaction.response.send_autocomplete(matching_options[:25])

def setup(bot):
    bot.add_cog(ServerSettingsCog(bot))
