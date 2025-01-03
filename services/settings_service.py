import nextcord
from numpy import place
from models.server_settings import ServerSettings
import yaml
from nextcord.ui import ChannelSelect

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class SettingsView(nextcord.ui.View):
    def __init__(self, settings_dict, server_id, bot, timeout=None):
        super().__init__(timeout=timeout)
        self.default_settings = config.get("server_settings", {})
        self.server_id = server_id
        self.bot = bot
        for setting, value in settings_dict.items():
            button_color = nextcord.ButtonStyle.success if value else nextcord.ButtonStyle.danger
            setting_label = format_setting(setting)
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

                        self.bot.update_setting(self.server_id, setting, setting_obj.setting_value)

                        button.style = nextcord.ButtonStyle.success if setting_obj.setting_value else nextcord.ButtonStyle.danger
                        print(self.bot.settings)
                        await interaction.response.edit_message(view=self)
                return button_callback

            button.callback = create_callback(setting, button)
            self.add_item(button)

class CategoriesView(nextcord.ui.View):
    def __init__(self, bot, server_id, timeout=None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.server_id = server_id
        self.default_settings = config.get("server_settings", {})
        for category in self.default_settings.keys():
            button = nextcord.ui.Button(label=format_setting(category), custom_id=category)
            
            async def callback(interaction: nextcord.Interaction, category=category):
                await interaction.response.send_message(
                    f"Settings for **{category}**:",
                    view=CategoryView(self.bot, self.server_id, category),
                    ephemeral=True
                )
            button.callback = callback
            self.add_item(button)

class CategoryView(nextcord.ui.View):
    def __init__(self, bot, server_id, category, timeout=None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.server_id = server_id
        self.category = category
        settings_dict = config["server_settings"][category]
        for setting, default_val in settings_dict.items():
            setting_name = f"{category}_{setting}"
            current_val = self.bot.settings[self.server_id].get(setting_name, str(default_val))
            if setting == "enabled":
                print(current_val)
                style = (nextcord.ButtonStyle.success if current_val == "True" else nextcord.ButtonStyle.danger)
                btn = nextcord.ui.Button(label="Enabled", style=style, custom_id=setting_name)
                async def toggle_callback(interaction: nextcord.Interaction, s=setting_name):
                    new_val = "False" if self.bot.settings[self.server_id][s] == "True" else "True"
                    # Check if enabling and if associated channel is set
                    if new_val == "True":
                        category = s.rsplit('_enabled', 1)[0]
                        channel_setting = f"{category}_channel"
                        channel_id = self.bot.settings[self.server_id].get(channel_setting, "None")
                        if channel_setting in self.bot.settings[self.server_id] and (channel_id == "None" or not channel_id):
                            await interaction.response.send_message(
                                f"**Error:** Please select a channel for `{format_setting(category)}` before enabling this setting.",
                                ephemeral=True
                            )
                            return
                    self.bot.update_setting(self.server_id, s, new_val)
                    ss = ServerSettings.get_or_none(
                        server_id=self.server_id, setting_name=s
                    )
                    if ss:
                        ss.setting_value = new_val
                        ss.save()
                    style2 = (nextcord.ButtonStyle.success if new_val == "True" else nextcord.ButtonStyle.danger)
                    btn.style = style2
                    await interaction.response.edit_message(view=self)
                btn.callback = toggle_callback
                self.add_item(btn)
            elif "_chance" in setting:
                btn = nextcord.ui.Button(
                    label=f"{format_setting(setting)} ({current_val})",
                    style=nextcord.ButtonStyle.secondary, custom_id=setting_name
                )
                async def chance_callback(interaction: nextcord.Interaction, s=setting_name, button_label=setting):
                    modal = ChanceModal(self.bot, self.server_id, s, parent_view=self, button_label=button_label)
                    await interaction.response.send_modal(modal)
                btn.callback = chance_callback
                self.add_item(btn)
            elif "channel" in setting:
                self.add_item(BotChannelSelect(bot, server_id, setting_name))

class ChanceModal(nextcord.ui.Modal):
    def __init__(self, bot, server_id, setting_name, parent_view, button_label):
        super().__init__(title="Edit Chance")
        self.bot = bot
        self.server_id = server_id
        self.setting_name = setting_name
        self.parent_view = parent_view
        self.chance_input = nextcord.ui.TextInput(label="New Chance Value", required=True)
        self.button_label = button_label
        self.add_item(self.chance_input)

    async def callback(self, interaction: nextcord.Interaction):
        new_val = self.chance_input.value
        self.bot.update_setting(self.server_id, self.setting_name, new_val)
        ss = ServerSettings.get_or_none(
            server_id=self.server_id, setting_name=self.setting_name
        )
        if ss:
            ss.setting_value = new_val
            ss.save()
        # Update the button label in the parent view
        for item in self.parent_view.children:
            if isinstance(item, nextcord.ui.Button) and item.custom_id == self.setting_name:
                item.label = f"{format_setting(self.button_label)} ({new_val})"
        await interaction.response.edit_message(view=self.parent_view)

class BotChannelSelect(ChannelSelect):
    def __init__(self, bot, server_id, setting_name):
        self.setting = ServerSettings.get_or_none(
            server_id=server_id, setting_name=setting_name
        )
        
        selected_channel = None
        
        if self.setting and self.setting.setting_value != "None":
            channel_id = self.setting.setting_value
            selected_channel = bot.get_channel(int(channel_id))
        
        placeholder = f"# {selected_channel.name}" if selected_channel else "Select a channel..."
            
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            channel_types=[nextcord.ChannelType.text],  # Restrict to text channels
        )
        self.bot = bot
        self.server_id = server_id
        self.setting_name = setting_name

    async def callback(self, interaction: nextcord.Interaction):
        selected_channel = self.values[0]  # The chosen channel object
        new_val = selected_channel.id  # Get the channel ID
        print(f"Selected Channel ID: {new_val}")
        self.bot.update_setting(self.server_id, self.setting_name, str(new_val))

        if self.setting:
            self.setting.setting_value = str(new_val)
            self.setting.save()

def get_setting(server_id, setting_name):
    setting = ServerSettings.get_or_none(
        ServerSettings.server_id == server_id,
        ServerSettings.setting_name == setting_name
    )
    
    return setting.setting_value if setting else None

def format_setting(setting_name):
    return setting_name.replace("_", " ").title()