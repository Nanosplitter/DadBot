import nextcord
from nextcord.ext import commands
from models.server_settings import ServerSettings
import yaml
from services.settings_service import CategoriesView

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class ServerSettingsCog(commands.Cog, name="server_settings"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="settings", description="Manage server settings.")
    async def settings(self, _: nextcord.Interaction):
        pass

    @settings.subcommand(name="edit", description="Edit the current server settings.")
    @commands.has_permissions(administrator=True)
    async def edit_settings(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        server_id = interaction.guild.id
        await interaction.followup.send(
            "Choose a setting category to edit:\n-# Colors of buttons won't update until this command is run again. Setting changes will be applied immediately.",
            view=CategoriesView(self.bot, server_id),
            ephemeral=True
        )

    @settings.subcommand(name="help", description="Get information about server settings.")
    async def settings_help(self, interaction: nextcord.Interaction):
        setting_descriptions = config["server_settings_descriptions"]
        
        help_message = "Here are the available server settings:\n"
        for setting, description in setting_descriptions.items():
            help_message += f"**{setting.replace('_', ' ').title()}** \n> {description}\n\n"
        
        await interaction.response.send_message(help_message)

    @settings.subcommand(name="reset", description="Reset server settings to default values.")
    @commands.has_permissions(administrator=True)
    async def reset_settings(self, interaction: nextcord.Interaction):
        server_id = interaction.guild.id
        default_settings = config["server_settings"]
        for setting_category, values in default_settings.items():
            for setting, default_value in values.items():
                setting_name = f"{setting_category}_{setting}"
                setting_obj, created = ServerSettings.get_or_create(
                    server_id=server_id,
                    server_name=interaction.guild.name,
                    setting_name=setting_name
                )

                setting_obj.setting_value = default_value
                setting_obj.save()
                self.bot.update_setting(server_id, setting_name, default_value)
        await interaction.response.send_message("Server settings have been reset to default values.")

def setup(bot):
    bot.add_cog(ServerSettingsCog(bot))
