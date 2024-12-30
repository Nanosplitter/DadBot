import nextcord
from models.server_settings import ServerSettings


class SettingsView(nextcord.ui.View):
    def __init__(self, settings_dict, server_id, timeout=None):
        super().__init__(timeout=timeout)
        self.server_id = server_id
        for setting, value in settings_dict.items():
            button_color = nextcord.ButtonStyle.success if value else nextcord.ButtonStyle.danger
            setting_label = setting.replace("_", " ").title()
            button = nextcord.ui.Button(label=setting_label, style=button_color, custom_id=setting)

            def create_callback(setting, button):
                async def button_callback(interaction: nextcord.Interaction):
                    setting_obj = ServerSettings.get_or_none(
                        ServerSettings.server_id == self.server_id,
                        ServerSettings.setting_name == setting
                    )
                    if setting_obj:
                        setting_obj.setting_value = not setting_obj.setting_value
                        setting_obj.save()

                        button.style = nextcord.ButtonStyle.success if setting_obj.setting_value else nextcord.ButtonStyle.danger
                        await interaction.response.edit_message(view=self)
                return button_callback

            button.callback = create_callback(setting, button)
            self.add_item(button)

def get_setting(server_id, setting_name):
    setting = ServerSettings.get_or_none(
        ServerSettings.server_id == server_id,
        ServerSettings.setting_name == setting_name
    )
    
    return setting.setting_value if setting else None