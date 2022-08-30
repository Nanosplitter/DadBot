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
class GPT(commands.Cog, name="gpt"):
    def __init__(self, bot):
        self.bot = bot

    # Here you can just add your own commands, you'll always need to provide "self" as first parameter.
    @commands.command(name="gpt")
    async def gpt(self, context, *text):
        """
        [Prompt] Generate a writing based on your prompt
        """
        await context.message.add_reaction("✅")
        
        api = PipelineCloud(token=config["pipeline_token"])
        run = api.run_pipeline(
            "pipeline_6908d8fb68974c288c69ef45454c8475",
            [
                " ".join(text),
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
        
        await context.reply(result)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(GPT(bot))
