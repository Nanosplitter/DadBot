import random
from typing import Optional
import mysql.connector
import openai
import yaml
import nextcord
import io
import os
import base64
from nextcord import Interaction, Embed, SlashOption
from nextcord.ext import commands

from noncommands.savedpersonalitiesutils import Personality, DeleteButton



with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Chat(commands.Cog, name="template"):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = config["openapi_token"]
        self.client = openai.OpenAI(api_key=config["openapi_token"])

    @nextcord.slash_command(name="chat", description="Chat with Dad")
    async def chat(
        self,
        interaction: Interaction,
        personality: Optional[str] = SlashOption(
            description="The personality or 'job' dad should have in this conversation",
            required=False,
        ),
        beef: Optional[bool] = SlashOption(
            description="If you want DadBot to think harder about his responses. He will respond much slower if enabled.",
            required=False,
            default=False,
        ),
    ):
        """
        [No Arguments] Chat with Dad.
        """

        response = "## Hey there! Let's chat!"

        if personality is not None:
            if personality.startswith("[saved_personality] "):
                mydb = mysql.connector.connect(
                    host=config["dbhost"],
                    user=config["dbuser"],
                    password=config["dbpassword"],
                    database=config["databasename"],
                    autocommit=True
                )

                mycursor = mydb.cursor(buffered=True)
                mycursor.execute("SELECT personality FROM personalities WHERE user_id = %s AND name = %s", (str(interaction.user.id), personality.replace("[saved_personality] ", "")))

                personality = mycursor.fetchone()[0]

                mycursor.close()
                mydb.close()

            response += f"\n\nCustom Personality: [{personality}]"
        if beef:
            response += "\n\nBeef: Enabled"

        partial_message = await interaction.response.send_message(response)

        message = await partial_message.fetch()

        try:
            if not interaction.user:
                await message.delete()
                await interaction.followup.send(
                    "I can't fetch your user data. Please try again.", ephemeral=True
                )
                return
            if not interaction.channel:
                await message.delete()
                await interaction.followup.send(
                    "I can't start a thread here! Make sure you're running this command in a channel.",
                    ephemeral=True,
                )
                return
            await message.create_thread(
                name=f"{interaction.user.display_name}'s Chat with Dad",
                auto_archive_duration=60,
            )
        except Exception as e:
            self.bot.logger.error(f"Error starting thread: {e}")
            await message.delete()
            await interaction.followup.send(
                "I can't start a thread here! Make sure you're running this command in a channel.",
                ephemeral=True,
            )
    
    @chat.on_autocomplete("personality")
    async def chat_autocomplete(self, interaction: Interaction, personality: str):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )

        mycursor = mydb.cursor(buffered=True)
        mycursor.execute("SELECT name FROM personalities WHERE user_id = %s", (str(interaction.user.id),))

        personality_names = [f"[saved_personality] {x[0]}" for x in mycursor]

        mycursor.close()

        mydb.close()

        personality_names = [i for i in personality_names if personality.lower() in i.lower()]

        await interaction.response.send_autocomplete(personality_names[:25])
    
    @nextcord.slash_command(name="personalities", description="default personalities command")
    async def personalities(self, interaction: Interaction):
        pass

    @personalities.subcommand(description="Create a personality")
    async def create(self, interaction: Interaction, name: str, personality: str):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("INSERT INTO personalities (user_id, name, personality) VALUES (%s, %s, %s)", (str(interaction.user.id), name, personality))

        personality = Personality(mycursor.lastrowid, interaction.user.id, name, personality)
        embed = personality.make_embed()

        await interaction.response.send_message(embed=embed)

        mydb.commit()
        mycursor.close()
        mydb.close()

    @personalities.subcommand(description="List your personalities")
    async def list(self, interaction: Interaction):
        mydb = mysql.connector.connect(
            host=config["dbhost"],
            user=config["dbuser"],
            password=config["dbpassword"],
            database=config["databasename"],
            autocommit=True
        )
        mycursor = mydb.cursor(buffered=True)

        mycursor.execute("SELECT * FROM personalities WHERE user_id = %s", (str(interaction.user.id),))

        

        firstReply = False
        for x in mycursor:
            personality = Personality(*x)

            view = nextcord.ui.View(timeout = None)

            view.add_item(DeleteButton(personality.id, personality.user_id))

            embed = personality.make_embed()
            if firstReply:
                await interaction.response.send_message(embed=embed, view=view)
            else:
                await interaction.channel.send(embed=embed, view=view)
                firstReply = True

        if not firstReply:
            await interaction.response.send_message("You don't have any personalities yet!")

        mydb.commit()
        mycursor.close()
        mydb.close()

def setup(bot):
    bot.add_cog(Chat(bot))
