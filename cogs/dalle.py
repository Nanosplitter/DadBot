import os
import sys
import yaml
from nextcord.ext import commands
import nextcord
from pipeline import PipelineCloud
import io, base64

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class Dalle(commands.Cog, name="dalle"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="dalle")
    async def Dalle(self, context, *text):
        """
        [Prompt] Generate 4 images based on your prompt
        """
        await context.message.add_reaction("✅")
        api = PipelineCloud(token=config["pipeline_token"])
        run = api.run_pipeline(
            "pipeline_17ac3021b7674b10a6fbe3cb980ff57d",
            [
                [" ".join(text)],
                {
                    "num_images": 4,  # must be a square number
                    "seed": -1,  # use a non-negative integer for deterministic sampling
                    "diversity": 3 # log2_supercondition_factor
                },
            ],
        )

        data = run["result_preview"][0][0]
        files = [nextcord.File(io.BytesIO(base64.b64decode(i)), filename="image.png") for i in data]
        
        await context.reply(files=files)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Dalle(bot))
