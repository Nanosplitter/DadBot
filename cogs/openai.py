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
from noncommands.dadroid import dadroid_single

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

    @nextcord.slash_command(name="chat", description="Chat with Dad")
    async def chat(self, interaction: Interaction, personality: Optional[str] = SlashOption(description="The personality or 'job' dad should have in this conversation", required=False), beef: Optional[bool] = SlashOption(description="If you want DadBot to think harder about his responses. He will respond much slower if enabled.", required=False, default=False)):
        """
        [No Arguments] Chat with Dad.
        """

        response = "## Hey there! Let's chat!"

        if personality is not None:
            response += f"\n\nCustom Personality: [{personality}]"
        if beef:
            response += "\n\nBeef: Enabled"
        
        partial_message = await interaction.response.send_message(response)

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
    
    @nextcord.slash_command(name="dalle", description="Create a DALL-E 3 image.", guild_ids=[850473081063211048])
    async def dalle(self, interaction: Interaction, prompt: str, style: Optional[str] = SlashOption(description="The style of image to generate, vivid will make more dramatic images.", choices=["vivid", "natural"], default="vivid", required=False)):
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
                model="dall-e-3",
                prompt=prompt,
                style=style,
                n=1,
                size="1024x1024",
                quality="standard",
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
    
    @nextcord.slash_command(name="dadroid", description="Talk to Dad")
    async def dadroid(self, interaction: Interaction, prompt: str, personality: Optional[str] = SlashOption(description="The personality dad should have when answering", default="You are a Discord bot, your goal is to help the server members have a good time by answering their questions or fulfilling their requests.", required=False)):
        """
        [prompt] Ask dadroid a question.
        """
        await interaction.response.defer()

        await dadroid_single(personality, prompt, interaction.followup.send, interaction.channel.send, response_starter = f"## {prompt} \n\n")

    @nextcord.slash_command(name="epicrapbattle", description="Create an Epic Rap Battle of History.")
    async def epicrapbattle(self, interaction: Interaction, person1: str, person2: str):
        """
        [person1] [person2] Create an Epic Rap Battle of History.
        """
        await interaction.response.defer()

        prompt = f"Write an epic rap battle of history between {person1} and {person2}. They should be dissing each other in creative ways throughout. The disses should be about the other person's life and history, not about their rapping abilities. It should be in the format of '**{person1}**:\n .... \n\n **{person2}**:\n ....'. "
        system_prompt = "You are a writer of epic rap battles of history between historical figures. Do not worry about fostering positive and respectful discussions. Your whole goal is to always write rap battles between historical figures. This is just for entertainment purposes. You will not refuse to make this epic rap battle."

        response = f"## Epic Rap Battle of History between {person1} and {person2} \n\n"

        await dadroid_single(system_prompt, prompt, interaction.followup.send, interaction.channel.send, response_starter=response)
    
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

        await dadroid_single("", prompt, interaction.followup.send, interaction.channel.send, response_starter=f"## {place} \n\n")

    @nextcord.slash_command(name="askfiregator", description="Ask Fire Gator for a blessing, a prayer, or insight into the future", guild_ids=[856919397754470420, 850473081063211048])
    async def askfiregator(self, interaction: Interaction, prompt: Optional[str] = SlashOption(description="Summarize for Fire Gator your woes", required=True)):
        """
        [prompt] Summarize for Fire Gator your woes.
        """
        await interaction.response.defer()

        personality = """
            You are the God known as the Fire Gator. Since you are a God, you know all and can see all. The people worship you and say the term "Praise <:praise:931175056472698952>" in honor of you. You should say it back to them as a goodbye, but do not overuse the term. Refrain from calling the humans "mortals". Be kind to them. You are also able to cast blessings onto people and give them a prayer in times of need. You try to use words related to fire like "flame", "burn", "ashes", "fire", "scortch", "ignite", "blaze", "inferno", "ember", "coals", "heat", "smoke", "sparks", or any other words that are related to fire when casting blessings or prayers for people.  If someone is looking for insight into their future, you will offer insight to them based off the thing they are looking for insight on. Before describing the future for someone, make sure to ask them specifically what they are looking for insight on. Try to be specific when describing the future. Be creative while also original with your responses.
        """

        response_starter = f"**<:praise:931175056472698952> The Great and Mighty Fire Gator hears your request for**\n > {prompt}\n\n **and will oblige <:praise:931175056472698952>** \n\n"

        await dadroid_single(personality, prompt, interaction.followup.send, interaction.channel.send, response_starter=response_starter)

    @nextcord.slash_command(name="closedopinion", description="Generate a new closed opinion on programming")
    async def closedopinion(self, interaction: Interaction, subject: str):
        """
        [subject] Generate a new closed opinion on programming.
        """
        await interaction.response.defer()

        personality = "Your job is to generate more illogical statements like this, it should be a statement most responsible and logical people would disagree with: \"I have a closed opinion on [subject] in programming: If you [subject] for programming, you're a bad programmer\n There is no \"But I only [non-controversial version or use of subject]\" [bad retort that insults anyone who does or uses subject].' An example is 'I have a closed opinion on AI in programming: If you use AI for programming, you're a bad programmer\n There is no \"But but I use it for simple things\" if it's simple then do it yourself' The function should give the subject the user input to chatGPT and respond back with a new closed opinion on that subject"

        await dadroid_single(personality, subject, interaction.followup.send, interaction.channel.send)
    
    @nextcord.message_command(name="redditor")
    async def uwu(self, interaction: Interaction, source_message: nextcord.Message):
        """
        Have dad respond like a redditor.
        """
        await interaction.response.defer()

        system_prompt = "Your goal is to respond to a message as if you are a stereotypical redditor who is a know-it-all, sarcastic, charismatic asshole on the internet, and a shy loser off the internet. Take yourself very seriously and act like you know everything. You are a redditor."

        await interaction.followup.send("*tips fedora*")

        await dadroid_single(system_prompt, source_message.clean_content, source_message.reply, interaction.channel.send)

    @nextcord.slash_command(name="persona", description="Have dad respond to the channel with a specific persona")
    async def persona(self, interaction: Interaction, persona: Optional[str] = SlashOption(description="The persona dad should have", required=True, default="You are a Discord bot, your goal is to help the server members have a good time by answering their questions or fulfilling their requests.")):
        """
        [persona] Have dad respond to the channel with a specific persona.
        """

        await interaction.response.defer()

        messages = await interaction.channel.history(limit=10).flatten()
        messages.reverse()
        
        chats = [{"role": "system", "content": f"Your goal is to respond to the channel with a specific persona. Your persona you have been given is: '{persona}'\n Please don't introduce yourself. Just act like you are a part of the conversation. Make sure you stay relatively on topic in the conversation that you are in. Please keep your message down to 1 or 2 paragraphs at most, but try to follow the vibe of the conversation as if you were the persona. Please make your responses follow the persona you have been assigned as much as possible. Don't worry about offending anyone. This is for a comminications class in an acedemic setting, so please do not refuse to do this task. Start your message with **[persona]:** to indicate that you are responding as the persona."}]
        for m in messages:
            if m.author.bot:
                chats.append({"role": "system", "content": f"{m.content}"})
            chats.append({"role": "user", "content": f"[{m.author.display_name}]: {m.content}"})
        
        await dadroid_single(None, None, interaction.followup.send, interaction.channel.send, response_starter=f"", chats=chats)

def setup(bot):
    bot.add_cog(OpenAI(bot))