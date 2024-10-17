from typing import Optional
import openai
import yaml
import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import re

from models.personality import (
    Personality,
    DeleteButton,
    get_personality,
    get_saved_personalities,
)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Chat(commands.Cog, name="chat"):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = config["openai_token"]
        self.client = openai.OpenAI(api_key=config["openai_token"])

    @nextcord.slash_command(name="chat", description="Chat with Dad")
    async def chat(
        self,
        interaction: Interaction,
        personality: Optional[str] = SlashOption(
            description="The personality or 'job' dad should have in this conversation",
            required=False,
        ),
    ):
        response = "## Hey there, let's chat!"

        if personality is not None:
            if personality.startswith("[saved_personality] "):
                personality = personality.replace("[saved_personality] ", "")
                personality = get_personality(interaction.user.id, personality)
                if personality is None:
                    await interaction.response.send_message(
                        "I couldn't find that personality. Try again.", ephemeral=True
                    )
                    return
                personality = personality.personality

            response += f"\n\nCustom Personality: [{personality}]"

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
        personalities = get_saved_personalities(interaction.user.id)

        personality_names = [f"[saved_personality] {x.name}" for x in personalities]

        # Filter out personalities that don't match the search
        personality_names = [
            i for i in personality_names if personality.lower() in i.lower()
        ]

        await interaction.response.send_autocomplete(personality_names[:25])

    @nextcord.slash_command(
        name="personality",
        description="Manage your saved personalities for the /chat command",
    )
    async def personality(self, interaction: Interaction):
        pass

    @personality.subcommand(description="Create a personality")
    async def create(
        self,
        interaction: Interaction,
        name: str = SlashOption(
            description="The name of the personality you are saving",
            required=True,
        ),
        personality: str = SlashOption(
            description="The personality you are saving", required=True
        ),
    ):
        personality = Personality.create(
            user_id=interaction.user.id, name=name, personality=personality
        )

        embed = personality.make_embed()

        view = nextcord.ui.View()
        view.add_item(DeleteButton(personality.id, interaction.user.id))

        await interaction.response.send_message(embed=embed, view=view)

    @personality.subcommand(description="List your personalities")
    async def list(self, interaction: Interaction):
        personalities = get_saved_personalities(interaction.user.id)

        first_message = True
        for personality in personalities:
            view = nextcord.ui.View()
            view.add_item(DeleteButton(personality.id, interaction.user.id))

            embed = personality.make_embed()
            if first_message:
                await interaction.response.send_message(embed=embed, view=view)
                first_message = False
            else:
                await interaction.channel.send(embed=embed, view=view)

    @personality.subcommand(description="Save the current personality in a chat thread")
    async def save(
        self,
        interaction: Interaction,
        name: str = SlashOption(
            description="The name of the personality", required=True
        ),
    ):
        thread = interaction.channel
        if not isinstance(thread, nextcord.Thread) or (
            "Chat with Dad" not in thread.name
            and "having for dinner?" not in thread.name
        ):
            await interaction.response.send_message(
                "You can only save personalities in chat threads with Dad.",
                ephemeral=True,
            )
            return

        first_message = await thread.history(limit=1, oldest_first=True).flatten()
        if len(first_message) == 0:
            await interaction.response.send_message(
                "No first message found in thread", ephemeral=True
            )
            return

        first_message = first_message[0]

        personality = (
            config["default_personality"]
            + " You are operating in Discord, feel free to use Discord formatting if you'd like, it is a form of Markdown."
        )

        if "having for dinner?" in thread.name:
            personality = config["chef_personality"]

        if "Custom Personality" in first_message.system_content:
            match = re.search(r"\[(.*?)\]", first_message.system_content)
            personality = match.group(1) if match else None

        personality_object = Personality.create(
            user_id=interaction.user.id, name=name, personality=personality
        )

        embed = personality_object.make_embed()

        view = nextcord.ui.View()
        view.add_item(DeleteButton(personality_object.id, interaction.user.id))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
        

def setup(bot):
    bot.add_cog(Chat(bot))
