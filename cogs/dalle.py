import os
import sys
import yaml
from pipeline import PipelineCloud
import io, base64
import nextcord
from typing import Optional
from nextcord.ext import commands
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Dalle(commands.Cog, name="dalle"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @nextcord.slash_command(name="dalle", description="Generate 4 images based on your prompt")
    async def Dalle(self, interaction: Interaction, prompt: str = SlashOption(description="A description of what you want to see.", required=True)):
        """
        [Prompt] Generate 4 images based on your prompt
        """
        message = await interaction.response.send_message("Generating images for '" + prompt + "'...")
        api = PipelineCloud(token=config["pipeline_token"])
        run = api.run_pipeline(
            "pipeline_17ac3021b7674b10a6fbe3cb980ff57d",
            [
                [prompt],
                {
                    "num_images": 4,  # must be a square number
                    "seed": -1,  # use a non-negative integer for deterministic sampling
                    "diversity": 3 # log2_supercondition_factor
                },
            ],
        )


        print(run["error"])
        if run["error"] == None:
            data = run["result_preview"][0][0]
            files = [nextcord.File(io.BytesIO(base64.b64decode(i)), filename="image.png") for i in data]
            await message.edit(content="Prompt: '" + prompt + "'", files=files)
        else:
            await message.edit(content="There was an error generating images for '" + prompt + "'. This is not your fault, please try again later.")
        

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Dalle(bot))
