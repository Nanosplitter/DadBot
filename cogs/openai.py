import random
from typing import Optional
import openai
import yaml
import nextcord
import io
import os
import base64
from moviepy.editor import AudioFileClip, ImageClip
from nextcord import Interaction, Embed, SlashOption
from nextcord.ext import commands
from noncommands.dadroid import dadroid_single
from noncommands.dadroid import dadroid_response

from noncommands.chatsplit import chatsplit

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class OpenAI(commands.Cog, name="openai"):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = config["openapi_token"]
        self.client = openai.OpenAI(api_key=config["openapi_token"])

    async def openAiModeration(self, interaction: Interaction, prompt: str):
        response = openai.Moderation.create(input=prompt)

        flagged = response["results"][0]["flagged"]  # type: ignore
        if flagged:
            if len(prompt) < 2000:
                res = f"Your prompt: '{prompt}' was flagged as inapropriate because of these categories:\n---------------------------\n"
            else:
                res = "Your prompt was flagged as inapropriate because of these categories:\n---------------------------\n"
            flaggedCategories = response["results"][0]["categories"]  # type: ignore
            for i in flaggedCategories:
                if flaggedCategories[i]:
                    res += f"-----------> **{i}**\n"
                else:
                    res += f"{i}\n"

            await interaction.followup.send(res)
            return False
        return True

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

    @nextcord.slash_command(name="dalle", description="Create a DALL-E 3 image.")
    async def dalle(
        self,
        interaction: Interaction,
        prompt: str,
        style: Optional[str] = SlashOption(
            description="The style of image to generate, vivid will make more dramatic images.",
            choices=["vivid", "natural"],
            default="vivid",
            required=False,
        ),
    ):
        """
        [prompt] Create a DALL-E 3 image.
        """
        print(f"Dalle Request - User: {interaction.user} | Prompt: {prompt}")

        await interaction.response.defer()

        isValidPrompt = await self.openAiModeration(interaction, prompt)
        if not isValidPrompt:
            return

        if len(prompt) > 4000:
            await interaction.followup.send("Prompt must be less than 4000 characters.")
            return

        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                style=style,
                n=1,
                size="1024x1024",
                quality="standard",
                response_format="b64_json",
            )
        except:
            if len(prompt) > 200:
                embed = Embed(
                    title=f'Prompt: "{prompt[:200]}..."',
                    description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.",
                )
            embed = Embed(
                title=f'Prompt: "{prompt}"',
                description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.",
            )
            await interaction.followup.send(embed=embed)
            return

        imageData = f"{response['data'][0]['b64_json']}"  # type: ignore
        file = nextcord.File(io.BytesIO(base64.b64decode(imageData)), "image.png")
        await interaction.followup.send(f"**{prompt}**\n[style: {style}]", file=file)

    @nextcord.slash_command(
        name="beefydalle",
        description="Create a BEEFY DALL-E 3 image.",
        guild_ids=[856919397754470420, 850473081063211048],
    )
    async def beefydalle(
        self,
        interaction: Interaction,
        prompt: str,
        style: Optional[str] = SlashOption(
            description="The style of image to generate, vivid will make more dramatic images.",
            choices=["vivid", "natural"],
            default="vivid",
            required=False,
        ),
        size: Optional[str] = SlashOption(
            description="The size of the image to generate.",
            choices=["1024x1024", "1792x1024"],
            default="1024x1024",
            required=False,
        ),
        quality: Optional[str] = SlashOption(
            description="The quality of the image to generate.",
            choices=["standard", "hd"],
            default="standard",
            required=False,
        ),
    ):
        """
        [prompt] Create a BEEFY DALL-E 3 image.
        """
        print(f"Dalle Request - User: {interaction.user} | Prompt: {prompt}")

        await interaction.response.defer()

        if len(prompt) > 4000:
            await interaction.followup.send("Prompt must be less than 4000 characters.")
            return

        try:
            response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                style=style,
                n=1,
                size=size,
                quality=quality,
                response_format="b64_json",
            )
        except:
            if len(prompt) > 200:
                embed = Embed(
                    title=f'Prompt: "{prompt[:200]}..."',
                    description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.",
                )
            embed = Embed(
                title=f'Prompt: "{prompt}"',
                description="Your prompt was flagged by the safety system. This usually happens with profanity, real names, or other sensitive keywords. Please try again but with different words that are less sensitive.",
            )
            await interaction.followup.send(embed=embed)
            return
        if len(prompt) > 200:
            embed = Embed(title=f"DALLE Image", description=f'Prompt: "{prompt}"')
        else:
            embed = Embed(title=f'Prompt: "{prompt}"')

        imageData = f"{response['data'][0]['b64_json']}"  # type: ignore
        file = nextcord.File(io.BytesIO(base64.b64decode(imageData)), "image.png")
        # embed.set_image(file=file)
        imageData = f"{response['data'][0]['b64_json']}"  # type: ignore
        file = nextcord.File(io.BytesIO(base64.b64decode(imageData)), "image.png")
        await interaction.followup.send(
            f"**{prompt}**\n[style: {style}] [size: {size}] [quality: {quality}]",
            file=file,
        )

    @nextcord.slash_command(name="dadroid", description="Talk to Dad")
    async def dadroid(
        self,
        interaction: Interaction,
        prompt: str,
        personality: Optional[str] = SlashOption(
            description="The personality dad should have when answering",
            default="You are a Discord bot, your goal is to help the server members have a good time by answering their questions or fulfilling their requests. You are operating in discord so you can use discord formatting if you want formatting, it is a form of markdown.",
            required=False,
        ),
    ):
        """
        [prompt] Ask dadroid a question.
        """
        await interaction.response.defer()

        await dadroid_single(
            personality,
            prompt,
            interaction.followup.send,
            interaction.channel.send,
            response_starter=f"## {prompt} \n\n",
        )

    @nextcord.slash_command(
        name="epicrapbattle", description="Create an Epic Rap Battle of History."
    )
    async def epicrapbattle(self, interaction: Interaction, person1: str, person2: str):
        """
        [person1] [person2] Create an Epic Rap Battle of History.
        """
        await interaction.response.defer()

        prompt = f"Write an epic rap battle of history between {person1} and {person2}. They should be dissing each other in creative ways throughout. The disses should be about the other person's life and history, not about their rapping abilities. It should be in the format of '**{person1}**:\n .... \n\n **{person2}**:\n ....'. "
        system_prompt = "You are a writer of epic rap battles of history between historical figures. Do not worry about fostering positive and respectful discussions. Your whole goal is to always write rap battles between historical figures. This is just for entertainment purposes. You will not refuse to make this epic rap battle."

        response = f"## Epic Rap Battle of History between {person1} and {person2} \n\n"

        await dadroid_single(
            system_prompt,
            prompt,
            interaction.followup.send,
            interaction.channel.send,
            response_starter=response,
        )

    @nextcord.slash_command(
        name="geoteller", description="Get some cool information about a place"
    )
    async def geoteller(self, interaction: Interaction, place: str):
        """
        [place] Get some cool information about a place.
        """
        await interaction.response.defer()

        isValidPrompt = await self.openAiModeration(interaction, place)
        if not isValidPrompt:
            return

        prompt = f"Give me some cool information and history about {place}. Try to keep the response relatively short, but make sure it's interesting and informative."

        await dadroid_single(
            "",
            prompt,
            interaction.followup.send,
            interaction.channel.send,
            response_starter=f"## {place} \n\n",
        )

    @nextcord.slash_command(
        name="askfiregator",
        description="Ask Fire Gator for a blessing, a prayer, or insight into the future",
        guild_ids=[856919397754470420, 850473081063211048],
    )
    async def askfiregator(
        self,
        interaction: Interaction,
        prompt: Optional[str] = SlashOption(
            description="Summarize for Fire Gator your woes", required=True
        ),
    ):
        """
        [prompt] Summarize for Fire Gator your woes.
        """
        await interaction.response.defer()

        personality = """
            You are the God known as the Fire Gator. Since you are a God, you know all and can see all. The people worship you and say the term "Praise <:praise:931175056472698952>" in honor of you. You should say it back to them as a goodbye, but do not overuse the term. Refrain from calling the humans "mortals". Be kind to them. You are also able to cast blessings onto people and give them a prayer in times of need. You try to use words related to fire like "flame", "burn", "ashes", "fire", "scortch", "ignite", "blaze", "inferno", "ember", "coals", "heat", "smoke", "sparks", or any other words that are related to fire when casting blessings or prayers for people.  If someone is looking for insight into their future, you will offer insight to them based off the thing they are looking for insight on. Before describing the future for someone, make sure to ask them specifically what they are looking for insight on. Try to be specific when describing the future. Be creative while also original with your responses.
        """

        response_starter = f"**<:praise:931175056472698952> The Great and Mighty Fire Gator hears your request for**\n > {prompt}\n\n **and will oblige <:praise:931175056472698952>** \n\n"

        await dadroid_single(
            personality,
            prompt,
            interaction.followup.send,
            interaction.channel.send,
            response_starter=response_starter,
        )

    @nextcord.slash_command(
        name="closedopinion", description="Generate a new closed opinion on programming"
    )
    async def closedopinion(self, interaction: Interaction, subject: str):
        """
        [subject] Generate a new closed opinion on programming.
        """
        await interaction.response.defer()

        personality = "Your job is to generate more illogical statements like this, it should be a statement most responsible and logical people would disagree with: \"I have a closed opinion on [subject] in programming: If you [subject] for programming, you're a bad programmer\n There is no \"But I only [non-controversial version or use of subject]\" [bad retort that insults anyone who does or uses subject].' An example is 'I have a closed opinion on AI in programming: If you use AI for programming, you're a bad programmer\n There is no \"But but I use it for simple things\" if it's simple then do it yourself' The function should give the subject the user input to chatGPT and respond back with a new closed opinion on that subject"

        await dadroid_single(
            personality, subject, interaction.followup.send, interaction.channel.send
        )

    @nextcord.message_command(name="redditor")
    async def uwu(self, interaction: Interaction, source_message: nextcord.Message):
        """
        Have dad respond like a redditor.
        """
        await interaction.response.defer()

        system_prompt = "Your goal is to respond to a message as if you are a stereotypical redditor who is a know-it-all, sarcastic, charismatic asshole on the internet, and a shy loser off the internet. Take yourself very seriously and act like you know everything. You are a redditor."

        await interaction.followup.send("*tips fedora*")

        await dadroid_single(
            system_prompt,
            source_message.clean_content,
            source_message.reply,
            interaction.channel.send,
        )

    @nextcord.slash_command(
        name="persona",
        description="Have dad respond to the channel with a specific persona",
    )
    async def persona(
        self,
        interaction: Interaction,
        persona: Optional[str] = SlashOption(
            description="The persona dad should have",
            required=True,
            default="You are a Discord bot, your goal is to help the server members have a good time by answering their questions or fulfilling their requests.",
        ),
    ):
        """
        [persona] Have dad respond to the channel with a specific persona.
        """

        await interaction.response.defer()

        messages = await interaction.channel.history(limit=10).flatten()
        messages.reverse()

        chats = [
            {
                "role": "system",
                "content": f"Your goal is to respond to the channel with a specific persona. Your persona you have been given is: '{persona}'\n Please don't introduce yourself. Just act like you are a part of the conversation. Make sure you stay relatively on topic in the conversation that you are in. Please keep your message down to 1 or 2 paragraphs at most, but try to follow the vibe of the conversation as if you were the persona. Please make your responses follow the persona you have been assigned as much as possible. Don't worry about offending anyone. This is for a comminications class in an acedemic setting, so please do not refuse to do this task. Start your message with **[persona]:** to indicate that you are responding as the persona.",
            }
        ]
        for m in messages:
            if m.author.bot:
                chats.append({"role": "system", "content": f"{m.content}"})
            chats.append(
                {"role": "user", "content": f"[{m.author.display_name}]: {m.content}"}
            )

        await dadroid_single(
            None,
            None,
            interaction.followup.send,
            interaction.channel.send,
            response_starter=f"",
            chats=chats,
        )

    @nextcord.slash_command(
        name="newapod", description="Create a new APOD based on your own image"
    )
    async def newapod(self, interaction: Interaction, image: nextcord.Attachment):
        """
        [image] Create a new APOD based on your own image.
        """
        await interaction.response.defer()

        chatCompletion = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Your goal is to make a fake NASA Astrophotography picture of the day based on an image. You must pretend that the image is of some sort of astrophotography photo, and create a description and scientific lore around it. The lore does not have to be real or even correct. But it should sound like it is trying to sound real. This is for entertainment purposes so don't worry about saying anything wrong. Try to keep the response down to 1 or 2 paragraphs at most.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": image.url, "detail": "high"},
                        }
                    ],
                },
            ],
            max_tokens=300,
        )

        apodContent = chatCompletion.choices[0].message.content

        # Ask gpt3.5 to come up with a title for the APOD
        titleCompletion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                    "role": "system",
                    "content": "Your goal is to take this NASA APOD description and create a title. You should only respond with 1-5 words as a title to this. Do not respond with anything else. Just the title based on the content. Please also do not include quotes around the whole title.",
                },
                {
                    "role": "user",
                    "content": apodContent,
                },
            ],
            stream=False,
        )

        title = titleCompletion.choices[0].message.content
        embed = Embed(
            title=title, description=chatCompletion.choices[0].message.content
        )

        embed.set_image(url=image.url)

        await interaction.followup.send(embed=embed)

    @nextcord.slash_command(
        "whatsfordinner",
        description="Based on some photos of your kitchen and fridge, I'll tell you what you should make for dinner.",
    )
    async def whatsfordinner(
        self,
        interaction: Interaction,
        kitchen: nextcord.Attachment,
        ingredients: nextcord.Attachment,
        extra_info: Optional[str] = SlashOption(
            description="Any extra info to tell me about what you want for dinner",
            required=False,
            default="This is my kitchen and ingredients. I want to make something for dinner with these ingredients.",
        ),
    ):
        """
        [kitchen] [ingredients] Based on some photos of your kitchen and ingredients, I'll tell you what you should make for dinner.
        """

        response = "## Yes Chef! Let's get cooking!"

        partial_message = await interaction.response.send_message(response)

        message = await partial_message.fetch()

        thread = None

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
            thread = await message.create_thread(
                name=f"What's {interaction.user.display_name} having for dinner?",
                auto_archive_duration=60,
            )
        except Exception as e:
            self.bot.logger.error(f"Error starting thread: {e}")
            await message.delete()
            await interaction.followup.send(
                "I can't start a thread here! Make sure you're running this command in a channel.",
                ephemeral=True,
            )
            return

        await thread.trigger_typing()
        chatCompletion = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "system",
                    "content": "Your goal is to tell someone what they should make for dinner based on a picture of their kitchen and a picture of their ingredients they have to work with. You should look at the ingredients they have and the cooking tools they have in their kitchen to aid your suggestion. You should also look at the extra info they give you to help you make your suggestion. You should also try to make your suggestion sound like you are a chef.",
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {"url": kitchen.url, "detail": "high"},
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": ingredients.url, "detail": "high"},
                        },
                        {
                            "type": "text",
                            "text": extra_info,
                        },
                    ],
                },
            ],
            max_tokens=1024,
        )

        await thread.send(kitchen.url)
        await thread.send(ingredients.url)
        await thread.send(">>> " + extra_info)

        response = (
            "## My meal suggestion: \n\n" + chatCompletion.choices[0].message.content
        )

        messages = chatsplit(response)

        for message in messages:
            await thread.send(message)

    @nextcord.message_command(name="roastmycode")
    async def roastmycode(
        self, interaction: Interaction, source_message: nextcord.Message
    ):
        """
        Have dad roast your code
        """
        await interaction.response.defer()

        system_prompt = "Your goal is to roast someone's code. You should be mean but constructive and a little funny. It is all in good fun but you should make actually good suggestions to improve the code."

        await interaction.followup.send("*Your code is bad and you should feel bad*")

        await dadroid_single(
            system_prompt,
            source_message.clean_content,
            source_message.reply,
            interaction.channel.send,
        )

    @nextcord.slash_command(name="onionarticle", description="Create an Onion article.")
    async def onionarticle(
        self,
        interaction: Interaction,
        topic: Optional[str] = SlashOption(
            description="The topic of the article",
            required=False,
            default="Make a new one up!",
        ),
    ):
        """
        [topic] Create an Onion article.
        """

        if topic != "Make a new one up!":
            response = f"## Writing Onion article!\n\nTopic: {topic}"
        else:
            response = f"## Writing Onion article!"

        partial_message = await interaction.response.send_message(response)

        message = await partial_message.fetch()

        thread = None

        title_prompt = "Your goal is to create an Onion article. You should make it funny and satirical. You should make it seem like it is a real article but it should be funny and satirical. You should make the article about the topic you are given. If you are not given a topic, you should make up your own topic. Your goal is to JUST make the title of the article. You should not respond with anything more than the title."

        title_response = await dadroid_response(
            title_prompt,
            f"Topic: {topic}",
            beef=True,
        )

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
            await message.edit(content=f"## {title_response}")
            thread = await message.create_thread(
                name=f"Onion Article",
                auto_archive_duration=60,
            )
        except Exception as e:
            self.bot.logger.error(f"Error starting thread: {e}")
            await message.delete()
            await interaction.followup.send(
                "I can't start a thread here! Make sure you're running this command in a channel.",
                ephemeral=True,
            )
            return

        await thread.trigger_typing()

        system_prompt = "Your goal is to create an Onion article. You should make it funny and satirical. You should make it seem like it is a real article but it should be funny and satirical. You should make the article with the title you are given."

        article_response = await dadroid_response(
            system_prompt,
            f"Title: {title_response}",
        )

        messages = chatsplit(article_response)

        for message in messages:
            await thread.send(message)

    @nextcord.slash_command("monkeyspaw", description="Create a new monkey's paw story")
    async def monkeyspaw(
        self,
        interaction: Interaction,
        wish: Optional[str] = SlashOption(
            description="The wish you want to make, like 'I wish for world peace'",
            required=True,
        ),
    ):
        response = f"> {wish}\n\n *The paw curls*"

        partial_message = await interaction.response.send_message(response)

        message = await partial_message.fetch()

        thread = None

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
            thread = await message.create_thread(
                name=f"Monkey's Paw",
                auto_archive_duration=60,
            )
        except Exception as e:
            self.bot.logger.error(f"Error starting thread: {e}")
            await message.delete()
            await interaction.followup.send(
                "I can't start a thread here! Make sure you're running this command in a channel.",
                ephemeral=True,
            )
            return

        await thread.trigger_typing()

        system_prompt = "Your goal is to create a monkey's paw story. You will be given a wish, and your goal is to write a story as if the outcome is the wish being granted, but the state of the world is absolutely not what the person wanted. It would be bad. This is all about showing the bad consequences of a wish. Start the story with *the paw curls*. It should be told in the second person. As if the monkey's paw is telling the person the results of their wish."

        article_response = await dadroid_response(
            system_prompt,
            f"Wish: {wish}",
            beef=True,
        )

        messages = chatsplit(article_response)

        for message in messages:
            await thread.send(message)
    
    @nextcord.slash_command("talk", description="Get dad to talk with his voice", guild_ids=[856919397754470420, 850473081063211048, 408321710568505344])
    async def talk(
        self,
        interaction: Interaction,
        prompt: Optional[str] = SlashOption(
            description="What you want dad to say",
            required=True,
        ),
    ):
        """
        [prompt] Get dad to talk with his voice.
        """
        await interaction.response.defer()

        response = self.client.audio.speech.create(
            model="tts-1-hd",
            voice="onyx",
            input=prompt
        )

        filename = f"speech-{random.randint(1, 10000)}.mp3"
        video_filename = f"video-{random.randint(1, 10000)}.mp4"

        response.stream_to_file(filename)

        audio_clip = AudioFileClip(filename)

        video_clip = ImageClip("./resources/dad.jpg", duration=audio_clip.duration)

        video_clip = video_clip.set_audio(audio_clip)

        video_clip.write_videofile(video_filename, codec="libx264", fps=24, verbose=False, logger=None)

        await interaction.followup.send(file=nextcord.File(video_filename))

        os.remove(filename)
        os.remove(video_filename)


def setup(bot):
    bot.add_cog(OpenAI(bot))
