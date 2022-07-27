import os
import sys

import nextcord
import yaml
from nextcord.ext import commands
from nextcord.ui import Button, View
if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Help(commands.Cog, name="help"):
    def __init__(self, bot):
        self.bot = bot

    def generateEmbedForCog(self, cog, prefix, index, max_index):
        """
        Generate an embed for a cog.
        """ 
        commands = cog.get_commands()
        command_list = [command.name for command in commands]
        command_description = [command.help for command in commands]

        embed = nextcord.Embed(title="Help: " + cog.qualified_name, description="List of available commands:", color=config["success"])
        for command, description in zip(command_list, command_description):
            embed.add_field(name=prefix + command, value=description)
        
        embed.set_footer(text=f"{index+1}/{max_index}")
        return embed

    @commands.command(name="help")
    async def help(self, context):
        """
        [No Arguments] List all commands from every Cog the bot has loaded.
        """
        prefix = config["bot_prefix"]
        if not isinstance(prefix, str):
            prefix = prefix[0]
        embed = nextcord.Embed(title="Help", description="List of available commands:", color=config["success"])
        cogs = [i for i in self.bot.cogs if i not in ["owner", "template", "moderation"]]

        count = len(cogs)
        index = 0
        currEmbed = self.generateEmbedForCog(self.bot.get_cog(cogs[index].lower()), prefix, index, count)

        previous_button = Button(label="<", style=nextcord.ButtonStyle.grey)

        async def previous_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) < 0:
                index = count - 1
            else:
                index = index - 1
            newembed = self.generateEmbedForCog(self.bot.get_cog(cogs[index].lower()), prefix, index, count)
            await interaction.message.edit(embed=newembed)
        
        next_button = Button(label=">", style=nextcord.ButtonStyle.blurple)

        async def next_callback(interaction):
            # edit the embed to show the previous result
            currEmbed = interaction.message.embeds[0].to_dict()
            index = int(currEmbed["footer"]["text"].split("/")[0]) - 1
            if (index + 1) >= count:
                index = 0
            else:
                index = index + 1
            newembed = self.generateEmbedForCog(self.bot.get_cog(cogs[index].lower()), prefix, index, count)
            await interaction.message.edit(embed=newembed)
        
        previous_button.callback = previous_callback
        next_button.callback = next_callback

        view = View(timeout=1000)
        view.add_item(previous_button)
        view.add_item(next_button)

        await context.send(embed=currEmbed, view=view)


def setup(bot):
    bot.add_cog(Help(bot))
