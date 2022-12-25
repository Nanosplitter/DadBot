import os
import openai
import yaml
import json
import nextcord
import io
import base64
from nextcord import Interaction, Embed
from nextcord.ext import commands

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class OpenAI(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = config["openapi_token"]
    
    async def openAiModeration(self, interaction: Interaction, prompt: str):
        response = openai.Moderation.create(
            input=prompt
        )
        
        flagged = response["results"][0]["flagged"]
        if flagged:
            if len(prompt) < 2000:
                res = f"Your prompt: '{prompt}' was flagged as inapropriate because of these categories:\n---------------------------\n"
            else:
                res = "Your prompt was flagged as inapropriate because of these categories:\n---------------------------\n"
            flaggedCategories = response["results"][0]["categories"]
            for i in flaggedCategories:
                if flaggedCategories[i]:
                    res += f"-----------> **{i}**\n"
                else:
                    res += f"{i}\n"

            await interaction.response.send_message(res)
            return False
        return True

    @nextcord.slash_command(name="dadroid", description="Talk to Dad")
    async def dadroid(self, interaction: Interaction, prompt: str):
        """
        [prompt] Ask dadroid a question.
        """
        isValidPrompt = await self.openAiModeration(interaction, prompt)
        if not isValidPrompt:
            return
        
        await interaction.response.defer()

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=300,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6
        )
        
        await interaction.followup.send(f"**{prompt}**{response['choices'][0]['text']}")
    
    @nextcord.slash_command(name="dalle", description="Create a DALL-E 2 image.")
    async def dalle(self, interaction: Interaction, prompt: str):
        """
        [prompt] Create a DALL-E 2 image.
        """
        print(f"Dalle Request - User: {interaction.user} | Prompt: {prompt}")
        isValidPrompt = await self.openAiModeration(interaction, prompt)
        if not isValidPrompt:
            return
        
        await interaction.response.defer()

        if len(prompt) > 1000:
            await interaction.followup.send("Prompt must be less than 1000 characters.")
            return

        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url"
            )
        except:
            embed = Embed(title=f'Prompt: "{prompt}"', description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.")
            await interaction.followup.send(embed=embed)
            return
        embed = Embed(title=f'Prompt: "{prompt}"')
        embed.set_image(url=response['data'][0]['url'])
        await interaction.followup.send(embed=embed)

def setup(bot):
    bot.add_cog(OpenAI(bot))