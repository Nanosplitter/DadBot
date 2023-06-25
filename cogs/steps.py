import os
import mysql.connector
import dateparser as dp
from dateparser.search import search_dates
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord.ui import Button, View, TextInput
from nextcord import Interaction, SlashOption, ChannelType, TextInput
from nextcord.abc import GuildChannel


from noncommands import birthdayLoop


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Steps(commands.Cog, name="steps"):
    def __init__(self, bot):
        self.bot = bot
    
    @nextcord.slash_command(name="logsteps", guild_ids=[850473081063211048])
    async def logsteps(self, interaction: Interaction):
        
        stepEmbed = await self.buildStepEmbed(interaction)

        log_steps_button = Button(label="Log Steps", style=nextcord.ButtonStyle.blurple)

        async def make_meme_button_callback(interaction):
            modal = self.StepLoggerModal()
        
            await interaction.response.send_modal(modal)

        log_steps_button.callback = make_meme_button_callback

        view = View(timeout=None)
        view.add_item(log_steps_button)
                
        await interaction.response.send_message(embed=stepEmbed, view=view)

    async def buildStepEmbed(self, interaction: Interaction):
        members = []
        
        if interaction.guild is None:
            await interaction.response.send_message("Sorry, I can't find your server information.")
            return
        
        for i in interaction.guild.members:
            members.append(str(i).split("#")[0])
        
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"]
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT user, SUM(steps) as steps FROM steplogs GROUP BY user ORDER BY steps DESC")
        
        rows = mycursor.fetchall()
        
        if rows is None:
            await interaction.response.send_message("No steps have been logged yet!")
            return

        stepEmbed = nextcord.Embed(title="Log your steps!", description="Current leaderboard:", color=0x00ff00)

        first = True
        
        for m in rows:
            if m[0].split("#")[0] in members:
                if first:
                    member = nextcord.utils.get(interaction.guild.members, name=m[0].split("#")[0])
                    stepEmbed.set_author(name=f"{m[0].split('#')[0]} is in the lead!", icon_url=f"{member.display_avatar.url}")
                    first = False
                stepEmbed.add_field(name=m[0].split("#")[0], value=f"{m[1]:,} steps", inline=False)
        
        mycursor.execute("SELECT * FROM steplogs WHERE steps = (SELECT MAX(steps) FROM steplogs) LIMIT 1")

        rows = mycursor.fetchall()

        if rows is None:
            await interaction.response.send_message("No steps have been logged yet!")
            return
        
        try:
            for m in rows:
                self.bot.logger.info(m)
                member = nextcord.utils.get(interaction.guild.members, name=m[2].split("#")[0])
                stepEmbed.set_footer(text=f"Single day record:\n {m[2].split('#')[0]} with {m[3]:,} steps", url=member.display_avatar.url)
        except AttributeError:
            self.bot.logger.error(f"Error getting member in step logger: {m}")

        mycursor.close()

        return stepEmbed
    
    class StepLoggerModal(nextcord.ui.Modal):
        def __init__(self, steps):
            super().__init__("Log your steps!")  # Modal title
            steps_input = TextInput(label=f"Steps", placeholder=f"10000", max_length=7, required=True)
            self.add_item(steps_input)
        
        async def callback(self, interaction: Interaction):
            mydb = mysql.connector.connect(
                host=config["dbhost"],
                user=config["dbuser"],
                password=config["dbpassword"],
                database=config["databasename"]
            )
            mycursor = mydb.cursor(buffered=True)

            mycursor.execute(f"INSERT INTO steplogs SET server_id = {interaction.guild.id}, user = '{interaction.user}', steps = {interaction.data['values']['steps']}, submit_time = NOW()")

            mydb.commit()
            mycursor.close()
            mydb.close()

            stepEmbed = await self.buildStepEmbed(interaction)

            await interaction.send(embed=stepEmbed)
        

def setup(bot):
    bot.add_cog(Steps(bot))
