import os
import platform
import nextcord
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


# Here we name the cog and create a new class for the cog.
class Info(commands.Cog, name="info"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="info", description="Get some useful (or not) information about the bot."
    )
    async def info(self, interaction: Interaction):
        """
        [No Arguments] Get some useful (or not) information about the bot.
        """
        embed = nextcord.Embed(description="The server's dad", color=config["success"])
        embed.set_author(name="Bot Information")
        embed.add_field(name="Owner:", value="nanosplitter", inline=True)
        embed.add_field(
            name="Python Version:", value=f"{platform.python_version()}", inline=True
        )
        embed.add_field(name="Prefix:", value=f"{config['bot_prefix']}", inline=False)
        embed.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="serverinfo",
        description="Get some useful (or not) information about the server.",
    )
    async def serverinfo(self, interaction: Interaction):
        """
        [No Arguments] Get some useful (or not) information about the server.
        """
        server = interaction.guild
        if server is None:
            await interaction.response.send_message(
                "Sorry, I can't find your server information."
            )
            return
        roles = [x.name for x in server.roles]
        role_length = len(roles)
        if role_length > 50:
            roles = roles[:50]
            roles.append(f">>>> Displaying[50/{len(roles)}] Roles")
        roles = ", ".join(roles)
        channels = len(server.channels)
        time = str(server.created_at)
        time = time.split(" ")
        time = time[0]

        embed = nextcord.Embed(
            title="**Server Name:**", description=f"{server}", color=config["success"]
        )

        if server.icon != None:
            embed.set_thumbnail(url=server.icon.url)
        embed.add_field(name="Server ID", value=server.id)
        embed.add_field(name="Member Count", value=server.member_count)
        embed.add_field(name="Text/Voice Channels", value=f"{channels}")
        embed.add_field(name=f"Roles ({role_length})", value=roles)
        embed.set_footer(text=f"Created at: {time}")
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(name="ping", description="Check if the bot is alive.")
    async def ping(self, interaction: Interaction):
        """
        [No Arguments] Check if the bot is alive.
        """
        embed = nextcord.Embed(color=config["success"])
        embed.add_field(name="Pong!", value=":ping_pong:", inline=True)
        embed.set_footer(text=f"Pong request by {interaction.user}")
        await interaction.response.send_message(embed=embed)

    @nextcord.slash_command(
        name="invite",
        description="Get the invite link of the Dad to be able to invite him to another server.",
    )
    async def invite(self, interaction: Interaction):
        """
        [No Arguments] Get the invite link of the Dad to be able to invite him to another server.
        """
        await interaction.response.send_message(
            f"Invite me by clicking here: https://discordapp.com/oauth2/authorize?&client_id={config['application_id']}&permissions=532576857152&scope=bot"
        )


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Info(bot))
