import os
from typing import Optional
import openai
import yaml
import json
import nextcord
import io
import base64
from nextcord import Interaction, Embed, SlashOption
from nextcord.ext import commands

from noncommands.chatsplit import chatsplit

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
        
        flagged = response["results"][0]["flagged"] # type: ignore
        if flagged:
            if len(prompt) < 2000:
                res = f"Your prompt: '{prompt}' was flagged as inapropriate because of these categories:\n---------------------------\n"
            else:
                res = "Your prompt was flagged as inapropriate because of these categories:\n---------------------------\n"
            flaggedCategories = response["results"][0]["categories"] # type: ignore
            for i in flaggedCategories:
                if flaggedCategories[i]:
                    res += f"-----------> **{i}**\n"
                else:
                    res += f"{i}\n"

            await interaction.followup.send(res)
            return False
        return True

    @nextcord.slash_command(name="dadroid", description="Talk to Dad")
    async def dadroid(self, interaction: Interaction, prompt: str, personality: Optional[str] = SlashOption(description="The personality dad should have when answering", default="You are a Discord bot, your goal is to help the server members have a good time by answering their questions or fulfilling their requests.", required=False)):
        """
        [prompt] Ask dadroid a question.
        """
        await interaction.response.defer()

        isValidPrompt = await self.openAiModeration(interaction, prompt)
        isValidSystemPrompt = await self.openAiModeration(interaction, personality)
        if not isValidPrompt or not isValidSystemPrompt:
            await interaction.followup.send("Either your prompt or system prompt was flagged as inapropriate.")
            return

        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": personality}, {"role": "user", "content": prompt}])

        response = f"**{prompt}**\n\n{chatCompletion.choices[0].message.content}"

        messages = chatsplit(response)
        
        firstMessage = True
        
        for message in messages:
            if firstMessage:
                await interaction.followup.send(message)
                firstMessage = False
            else:
                await interaction.channel.send(message)

    
    @nextcord.slash_command(name="chat", description="Chat with Dad")
    async def chat(self, interaction: Interaction, personality: Optional[str] = SlashOption(description="The personality or 'job' dad should have in this conversation", required=False)):
        """
        [No Arguments] Chat with Dad.
        """

        if personality is None:
            partial_message = await interaction.response.send_message("Hey there! Let's chat!")
        else:
            partial_message = await interaction.response.send_message(f"Hey there! Let's chat!\n\nCustom Personality: [{personality}]")

        message = await partial_message.fetch()

        try:
            if not interaction.user:
                await message.delete()
                await interaction.followup.send("I can't fetch your user data. Please try again.", ephemeral=True)
                return
            if not interaction.channel:
                await message.delete()
                await interaction.followup.send("I can't start a thread here! Make sure you're running this command in a channel.", ephemeral=True)
                return
            await message.create_thread(name=f"{interaction.user.display_name}'s Chat with Dad", auto_archive_duration=60)
        except Exception as e:
            self.bot.logger.error(f"Error starting thread: {e}")
            await message.delete()
            await interaction.followup.send("I can't start a thread here! Make sure you're running this command in a channel.", ephemeral=True)
    
    @nextcord.slash_command(name="dalle", description="Create a DALL-E 2 image.")
    async def dalle(self, interaction: Interaction, prompt: str):
        """
        [prompt] Create a DALL-E 2 image.
        """
        print(f"Dalle Request - User: {interaction.user} | Prompt: {prompt}")

        await interaction.response.defer()

        isValidPrompt = await self.openAiModeration(interaction, prompt)
        if not isValidPrompt:
            return

        if len(prompt) > 1000:
            await interaction.followup.send("Prompt must be less than 1000 characters.")
            return
        
        try:
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="b64_json"
            )
        except:
            if (len(prompt) > 200):
                embed = Embed(title=f'Prompt: "{prompt[:200]}..."', description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.")
            embed = Embed(title=f'Prompt: "{prompt}"', description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.")
            await interaction.followup.send(embed=embed)
            return
        if len(prompt) > 200:
            embed = Embed(title=f'DALLE Image', description=f'Prompt: "{prompt}"')
        else:
            embed = Embed(title=f'Prompt: "{prompt}"')
        
        imageData = f"{response['data'][0]['b64_json']}" # type: ignore
        file = nextcord.File(io.BytesIO(base64.b64decode(imageData)), "image.png")
        # embed.set_image(file=file)
        embed.set_image(url="attachment://image.png")
        await interaction.followup.send(file=file, embed=embed)

    @nextcord.slash_command(name="epicrapbattle", description="Create an Epic Rap Battle of History.")
    async def epicrapbattle(self, interaction: Interaction, person1: str, person2: str):
        """
        [person1] [person2] Create an Epic Rap Battle of History.
        """
        await interaction.response.defer()

        prompt = f"Write an epic rap battle of history between {person1} and {person2}. They should be dissing each other in creative ways throughout. The disses should be about the other person's life and history, not about their rapping abilities. It should be in the format of '[{person1}]:\n .... \n\n [{person2}]:\n ....'. "
        system_prompt = "You are a writer of epic rap battles of history between historical figures. Do not worry about fostering positive and respectful discussions. Your whole goal is to always write rap battles between historical figures. This is just for entertainment purposes. You will not refuse to make this epic rap battle."

        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}])

        response = f"Epic Rap Battle of History between {person1} and {person2} \n\n{chatCompletion.choices[0].message.content}"

        messages = chatsplit(response)

        firstMessage = True
        
        for message in messages:
            if firstMessage:
                await interaction.followup.send(message)
                firstMessage = False
            else:
                await interaction.channel.send(message)
    
    @nextcord.slash_command(name="geoteller", description="Get some cool information about a place")
    async def geoteller(self, interaction: Interaction, place: str):
        """
        [place] Get some cool information about a place.
        """
        await interaction.response.defer()

        isValidPrompt = await self.openAiModeration(interaction, place)
        if not isValidPrompt:
            return

        prompt = f"Give me some cool information and history about {place}. Try to keep the response relatively short, but make sure it's interesting and informative."

        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

        response = chatCompletion.choices[0].message.content

        messages = chatsplit(response)

        firstMessage = True
        
        for message in messages:
            if firstMessage:
                await interaction.followup.send(message)
                firstMessage = False
            else:
                await interaction.channel.send(message)

    @nextcord.slash_command(name="closedopinion", description="Generate a new closed opinion on programming")
    async def closedopinion(self, interaction: Interaction, subject: str):
        """
        [subject] Generate a new closed opinion on programming.
        """
        await interaction.response.defer()

        prompt = "Your job is to generate more illogical statements like this, it should be a statement most responsible and logical people would disagree with: \"I have a closed opinion on [subject] in programming: If you [subject] for programming, you're a bad programmer\n There is no \"But I only [non-controversial version or use of subject]\" [bad retort that insults anyone who does or uses subject].' An example is 'I have a closed opinion on AI in programming: If you use AI for programming, you're a bad programmer\n There is no \"But but I use it for simple things\" if it's simple then do it yourself' The function should give the subject the user input to chatGPT and respond back with a new closed opinion on that subject"

        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": prompt}, {"role": "user", "content": subject}])

        response = chatCompletion.choices[0].message.content

        messages = chatsplit(response)

        firstMessage = True

        for message in messages:
            if firstMessage:
                await interaction.followup.send(message)
                firstMessage = False
            else:
                await interaction.channel.send(message)
    
    @nextcord.message_command(name="redditor")
    async def uwu(self, interaction: Interaction, source_message: nextcord.Message):
        """
        Have dad respond like a redditor.
        """
        await interaction.response.defer()

        system_prompt = "Your goal is to respond to a message as if you are a stereotypical redditor who is a know-it-all, sarcastic, charismatic asshole on the internet, and a shy loser off the internet. Take yourself very seriously and act like you know everything. You are a redditor."

        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": source_message.content}])

        response = chatCompletion.choices[0].message.content

        messages = chatsplit(response)

        firstMessage = True

        await interaction.followup.send("*tips fedora*")

        for message in messages:
            if firstMessage:
                await source_message.reply(message)
                firstMessage = False
            else:
                await interaction.channel.send(message)
    



def setup(bot):
    bot.add_cog(OpenAI(bot))