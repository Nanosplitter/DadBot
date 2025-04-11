import nextcord
from models.server_settings import ServerSettings
import yaml
from nextcord.ui import ChannelSelect

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class SettingsView(nextcord.ui.View):
    def __init__(self, initial_settings, server_id, bot, timeout=None):
        super().__init__(timeout=timeout)
        self.default_settings = config.get("server_settings", {})
        self.server_id = server_id
        self.bot = bot
        for option_name, is_active in initial_settings.items():
            button_style = nextcord.ButtonStyle.success if is_active else nextcord.ButtonStyle.danger
            button_label = to_title_case(option_name)
            button = nextcord.ui.Button(label=button_label, style=button_style, custom_id=option_name)
            button.callback = lambda interaction, option_name=option_name, button=button: self.toggle_button_callback(interaction, option_name, button)
            self.add_item(button)

    async def toggle_button_callback(self, interaction: nextcord.Interaction, name: str, btn: nextcord.ui.Button):
        found_setting = ServerSettings.get_or_none(
            ServerSettings.server_id == self.server_id,
            ServerSettings.setting_name == name
        )
        
        if found_setting:
            found_setting.setting_value = not found_setting.setting_value
            found_setting.save()
            self.bot.update_setting(self.server_id, name, found_setting.setting_value)
            btn.style = (
                nextcord.ButtonStyle.success if found_setting.setting_value
                else nextcord.ButtonStyle.danger
            )
            await interaction.response.edit_message(view=self)

class CategoriesView(nextcord.ui.View):
    def __init__(self, bot, server_id, timeout=None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.server_id = server_id
        self.default_settings = config.get("server_settings", {})
        for category_name in self.default_settings.keys():
            is_enabled = str(self.bot.settings[self.server_id].get(f"{category_name}_enabled", self.default_settings[category_name]["enabled"])) == "True"
            style = nextcord.ButtonStyle.success if is_enabled else nextcord.ButtonStyle.danger
            category_button = nextcord.ui.Button(label=to_title_case(category_name), custom_id=category_name, style=style)
            category_button.callback = lambda i, c=category_name: self.select_category_callback(i, c)
            self.add_item(category_button)

    async def select_category_callback(self, interaction: nextcord.Interaction, cat: str):
        await interaction.response.send_message(
            f"Settings for **{to_title_case(cat)}**:\n> {config['server_settings_descriptions'][cat]}",
            view=CategoryView(self.bot, self.server_id, cat),
            ephemeral=True
        )

class CategoryView(nextcord.ui.View):
    def __init__(self, bot, server_id, category_name, timeout=None):
        super().__init__(timeout=timeout)
        self.bot = bot
        self.server_id = server_id
        self.category = category_name
        category_defaults = config["server_settings"][category_name]
        for option, default_value in category_defaults.items():
            option_name = f"{category_name}_{option}"
            current_value = self.bot.settings[self.server_id].get(option_name, str(default_value))
            if option == "enabled":
                
                enabled = str(current_value) == "True"
                
                style = nextcord.ButtonStyle.success if enabled else nextcord.ButtonStyle.danger
                label = "Enabled" if enabled else "Disabled"
                
                enable_button = nextcord.ui.Button(label=label, style=style, custom_id=option_name)
                enable_button.callback = lambda interaction, option_name=option_name, button=enable_button: self.toggle_enabled_setting_callback(interaction, option_name, button)
                self.add_item(enable_button)
            elif "_chance" in option:
                chance_button = nextcord.ui.Button(
                    label=f"{to_title_case(option)} ({current_value}%)",
                    style=nextcord.ButtonStyle.secondary,
                    custom_id=option_name
                )
                chance_button.callback = lambda interaction, option_name=option_name, label=option: self.change_chance_callback(interaction, option_name, label)
                self.add_item(chance_button)
            elif "channel" in option:
                self.add_item(ChannelSelector(bot, server_id, option_name))

    async def toggle_enabled_setting_callback(self, interaction: nextcord.Interaction, opt: str, enable_button: nextcord.ui.Button):
        new_value = "False" if str(self.bot.settings[self.server_id][opt]) == "True" else "True"
        if new_value == "True":
            setting_prefix = opt.rsplit('_enabled', 1)[0]
            channel_option = f"{setting_prefix}_channel"
            channel_id = self.bot.settings[self.server_id].get(channel_option, "None")
            if channel_option in self.bot.settings[self.server_id] and (channel_id == "None" or not channel_id):
                await interaction.response.send_message(
                    f"**Error:** Please select a channel for `{to_title_case(setting_prefix)}` before enabling this setting.",
                    ephemeral=True
                )
                return
        self.bot.update_setting(self.server_id, opt, new_value)
        found_setting = ServerSettings.get_or_none(server_id=self.server_id, setting_name=opt)
        if found_setting:
            found_setting.setting_value = new_value
            found_setting.save()
        is_enabled = new_value == "True"
        enable_button.style = nextcord.ButtonStyle.success if is_enabled else nextcord.ButtonStyle.danger
        enable_button.label = "Enabled" if is_enabled else "Disabled"
        await interaction.response.edit_message(view=self)

    async def change_chance_callback(self, interaction: nextcord.Interaction, opt: str, button_label: str):
        modal = ChanceEditModal(self.bot, self.server_id, opt, parent_view=self, button_label=button_label)
        await interaction.response.send_modal(modal)

class ChanceEditModal(nextcord.ui.Modal):
    def __init__(self, bot, server_id, setting_name, parent_view, button_label):
        super().__init__(title="Edit Chance")
        self.bot = bot
        self.server_id = server_id
        self.setting_name = setting_name
        self.parent_view = parent_view
        self.button_label = button_label
        self.chance_input = nextcord.ui.TextInput(label="New Chance Value", required=True, placeholder="Enter a number between 0 and 100", min_length=1, max_length=3)
        self.add_item(self.chance_input)

    async def callback(self, interaction: nextcord.Interaction):
        new_value = self.chance_input.value
        
        try:
            parsed_value = int(new_value)
            if parsed_value < 0 or parsed_value > 100:
                await interaction.response.send_message(
                    "Please enter a chance between 0 and 100.", ephemeral=True
                )
                return
        except ValueError:
            await interaction.response.send_message(
                "Please enter a whole number for chance.", ephemeral=True
            )
            return
        
        self.bot.update_setting(self.server_id, self.setting_name, str(parsed_value))
        
        found_setting = ServerSettings.get_or_none(
            server_id=self.server_id, setting_name=self.setting_name
        )
        
        if found_setting:
            found_setting.setting_value = str(parsed_value)
            found_setting.save()

        for item in self.parent_view.children:
            if isinstance(item, nextcord.ui.Button) and item.custom_id == self.setting_name:
                item.label = f"{to_title_case(self.button_label)} ({parsed_value}%)"
                
        await interaction.response.edit_message(view=self.parent_view)

class ChannelSelector(ChannelSelect):
    def __init__(self, bot, server_id, setting_name):
        self.setting = ServerSettings.get_or_none(server_id=server_id, setting_name=setting_name)
        channel_instance = None
        if self.setting and self.setting.setting_value != "None":
            channel_id = self.setting.setting_value
            channel_instance = bot.get_channel(int(channel_id))
        placeholder_value = f"# {channel_instance.name}" if channel_instance else "Select a channel..."
        super().__init__(
            placeholder=placeholder_value,
            min_values=1,
            max_values=1,
            channel_types=[nextcord.ChannelType.text]
        )
        self.bot = bot
        self.server_id = server_id
        self.setting_name = setting_name

    async def callback(self, interaction: nextcord.Interaction):
        channel_instance = self.values[0]
        new_value = channel_instance.id
        self.bot.update_setting(self.server_id, self.setting_name, str(new_value))
        if self.setting:
            self.setting.setting_value = str(new_value)
            self.setting.save()

def get_setting(server_id, setting_name):
    found_setting = ServerSettings.get_or_none(
        ServerSettings.server_id == server_id,
        ServerSettings.setting_name == setting_name
    )
    return found_setting.setting_value if found_setting else None

def to_title_case(name):
    return name.replace("_", " ").title()