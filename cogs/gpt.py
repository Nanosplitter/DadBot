import os
import sys
import yaml
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from pipeline import PipelineCloud
import io, base64


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class GPT(commands.Cog, name="gpt"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @nextcord.slash_command(name="gpt", description="Generate a writing based on your prompt")
    async def gpt(self, interaction: Interaction, prompt: str = SlashOption(description="A prompt for dad to finish using GPT", required=True)):
        """
        [Prompt] Generate a writing based on your prompt
        """
        message = await interaction.response.send_message("Generating response for '" + prompt + "'...")
        
        api = PipelineCloud(token=config["pipeline_token"])
        run = api.run_pipeline(
            "pipeline_6908d8fb68974c288c69ef45454c8475",
            [
                prompt,
                {
                    "response_length": 300,  # how many new tokens to generate
                    "include_input": True,  # set to True if you want the response to contain your input
                    "temperature": 1.0,
                    "top_k": 50
                    # most params from the transformers library "generate" function are supported
                },
            ],
        )

        result = run["result_preview"][0][0]
        
        await message.edit(result.replace(prompt, "**" + prompt + "**"))

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(GPT(bot))
