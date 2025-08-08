import yaml
import nextcord
from nextcord import Interaction
from nextcord.ext import commands
from noncommands.chatsplit import chat_split
from noncommands.chat import Chat
import openai

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Translate(commands.Cog, name="translate"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.message_command(name="translate")
    async def translate(self, interaction: Interaction, message: nextcord.Message):
        """
        Translate a message to English.
        """

        await interaction.response.defer()

        client = openai.OpenAI(api_key=config["openapi_token"])
        chat = Chat(self.bot)
        prepared_messages = await chat.prepare_chat_messages([message])

        response = client.responses.create(
            model="gpt-5",
            instructions="You are a translator. Your goal is to translate the following message to english. Only reply with the translation and nothing else. If the message is an image, translate the text in the image to english.",
            input=prepared_messages[0],
        )

        translation_response = (
            f"Translation of: {message.jump_url}\n >>> {response.output_text}"
        )

        for message in chat_split(translation_response):
            await interaction.followup.send(message, suppress_embeds=True)


def setup(bot):
    bot.add_cog(Translate(bot))
