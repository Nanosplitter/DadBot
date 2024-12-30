import nextcord
from nextcord.ext import commands
from models.server_settings import ServerSettings
import yaml
from services.settings_service import SettingsView

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class ServerSettingsCog(commands.Cog, name="server_settings"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="settings", description="Manage server settings.", guild_ids=[850473081063211048])
    async def settings(self, interaction: nextcord.Interaction):
        pass

    @settings.subcommand(name="view", description="View the current server settings.")
    @commands.has_permissions(administrator=True)
    async def view_settings(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        settings = ServerSettings.select().where(ServerSettings.server_id == server_id)
        if settings.exists():
            settings_dict = {s.setting_name: s.setting_value for s in settings}
            view = SettingsView(settings_dict, server_id)
            await interaction.response.send_message("Current settings:", view=view)
        else:
            await interaction.response.send_message("No settings found for this server.")

    @settings.subcommand(name="reset", description="Reset server settings to default values.")
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        default_settings = config["default_server_settings"]
        print(default_settings)
        for setting, value in default_settings.items():
            setting_obj, created = ServerSettings.get_or_create(
                server_id=server_id,
                setting_name=setting,
                defaults={'setting_value': value}
            )
            print(setting_obj)
            setting_obj.save()
        await interaction.response.send_message("Server settings have been reset to default values.")

def setup(bot):
    bot.add_cog(ServerSettingsCog(bot))
