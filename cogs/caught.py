import yaml
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from services.db_service import *
from models.caught import get_all_in_server, Caught

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Caught(commands.Cog, name="caught"):
    def __init__(self, bot):
        self.bot = bot
        self.old_names = dict()

    @nextcord.slash_command(name="caught", description="See how many times everyone on the server has been caught by DadBot.")
    async def caught(self, interaction: Interaction):
        """
        [No Arguments] See how many times everyone on the server has been caught by DadBot.
        """
        
        if interaction.guild is None:
            await interaction.response.send_message("Sorry, I can't find your server information.")
            return

        embeds = []
        position = 0

        position_colors = {
            0: 0xffd700,
            1: 0xc0c0c0,
            2: 0xcd7f32
        }

        for caught in get_all_in_server(interaction.guild.members):
            member = nextcord.utils.get(interaction.guild.members, id=int(caught.user_id))

            if position < 3:
                embed = nextcord.Embed(title="", color=position_colors[position])
                position += 1
            else:
                embed = nextcord.Embed(title="")

            if member is not None:
                embed = caught.build_embed(member, embed.color)
                embeds.append(embed)

        if len(embeds) == 0:
            await interaction.response.send_message("No one has been caught yet! \nTry running `/fixcaughtids` if you expected stuff to show up here.")
            return

        firstMessage = True

        embed_group = []
        for embed in embeds:
            embed_group.append(embed)
            if len(embed_group) == 9:
                if firstMessage:
                    await interaction.response.send_message(embeds=embed_group)
                    firstMessage = False
                else:
                    await interaction.channel.send(embeds=embed_group)
                embed_group = []

        if len(embed_group) > 0:
            if firstMessage:
                await interaction.response.send_message(embeds=embed_group)
            else:
                await interaction.channel.send(embeds=embed_group)

def setup(bot):
    bot.add_cog(Caught(bot))
