from typing import Optional
import openai
import yaml
import nextcord
import io
import base64
import aiohttp
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from noncommands.dadroid import dadroid_single
from noncommands.dadroid import dadroid_response
from pdfminer.high_level import extract_text

from noncommands.chatsplit import chat_split

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class AiStuff(commands.Cog, name="aistuff"):
    def __init__(self, bot):
        self.bot = bot
        openai.api_key = config["openapi_token"]
        self.client = openai.OpenAI(api_key=config["openapi_token"])

    @nextcord.slash_command(name="image", description="Get an image from a prompt")
    async def image(
        self,
        interaction: Interaction,
        prompt: Optional[str] = SlashOption(
            description="The prompt to generate the image from.",
            required=True,
        ),
    ):
        await interaction.response.defer()
        try:
            quality = "medium"
            if interaction.user.id == 776256478877057035:
                quality = "high"
            img = self.client.images.generate(
                model="gpt-image-1",
                prompt=prompt,
                n=1,
                size="auto",
                quality=quality,
            )
            image_bytes = base64.b64decode(img.data[0].b64_json)
            image_file = io.BytesIO(image_bytes)
            await interaction.followup.send(
                f"**Prompt:** {prompt}",
                file=nextcord.File(image_file, filename="image.png"),
            )
        except openai.BadRequestError as e:
            await interaction.followup.send(
                f"An error occurred while generating the image: {e}"
            )

    @nextcord.slash_command(
        name="dalle", description="Deprecated commad for DALL-E, use /image instead"
    )
    async def dalle(
        self,
        interaction: Interaction,
    ):
        await interaction.response.send_message(
            "This command is deprecated. Use </image:1372592282456555550> instead!",
            ephemeral=True,
        )

    @nextcord.slash_command(
        name="dadroid", description="Deprecated command, use /chat instead"
    )
    async def dadroid(self, interaction: Interaction):
        await interaction.response.send_message(
            "This command is deprecated. Use </chat:1205212799597547633> instead!",
            ephemeral=True,
        )

    @nextcord.slash_command(
        name="epicrapbattle", description="Create an Epic Rap Battle of History."
    )
    async def epicrapbattle(
        self,
        interaction: Interaction,
        person1: Optional[str] = SlashOption(
            description="Person 1 in the rap battle",
            required=True,
        ),
        person2: Optional[str] = SlashOption(
            description="Person 2 in the rap battle",
            required=True,
        ),
    ):
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
        name="closedopinion",
        description="Generate a new closed opinion on programming",
        guild_ids=[850473081063211048, 856919397754470420],
    )
    async def closedopinion(
        self,
        interaction: Interaction,
        subject: Optional[str] = SlashOption(
            description="The subject of the closed opinion.",
            required=True,
        ),
    ):
        """
        [subject] Generate a new closed opinion on programming.
        """
        await interaction.response.defer()

        personality = "Your job is to generate more illogical statements like this, it should be a statement most responsible and logical people would disagree with: \"I have a closed opinion on [subject] in programming: If you [subject] for programming, you're a bad programmer\n There is no \"But I only [non-controversial version or use of subject]\" [bad retort that insults anyone who does or uses subject].' An example is 'I have a closed opinion on AI in programming: If you use AI for programming, you're a bad programmer\n There is no \"But but I use it for simple things\" if it's simple then do it yourself' The function should give the subject the user input to chatGPT and respond back with a new closed opinion on that subject"

        await dadroid_single(
            personality, subject, interaction.followup.send, interaction.channel.send
        )

    # @nextcord.message_command(name="redditor")
    # async def uwu(self, interaction: Interaction, source_message: nextcord.Message):
    #     """
    #     Have dad respond like a redditor to a message.
    #     """
    #     await interaction.response.defer()

    #     system_prompt = "Your goal is to respond to a message as if you are a stereotypical redditor who is a know-it-all, sarcastic, charismatic asshole on the internet, and a shy loser off the internet. Take yourself very seriously and act like you know everything. You are a redditor."

    #     await interaction.followup.send("*tips fedora*")

    #     await dadroid_single(
    #         system_prompt,
    #         source_message.clean_content,
    #         source_message.reply,
    #         interaction.channel.send,
    #     )

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
            response_starter="",
            chats=chats,
        )

    @nextcord.slash_command(
        name="newapod", description="Create a new APOD based on your own image"
    )
    async def newapod(
        self,
        interaction: Interaction,
        image: Optional[nextcord.Attachment] = SlashOption(
            description="The image to base the APOD on.", required=True
        ),
    ):
        """
        [image] Create a new APOD based on your own image.
        """
        await interaction.response.defer()

        chatCompletion = self.client.chat.completions.create(
            model="gpt-5",
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
        )

        apodContent = chatCompletion.choices[0].message.content

        titleCompletion = self.client.chat.completions.create(
            model="gpt-5",
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

        title = "# APOD - " + titleCompletion.choices[0].message.content + "\n"
        explanation = ">>> " + apodContent + "\n"

        async with aiohttp.ClientSession() as session:
            async with session.get(image.url) as resp:
                if resp.status == 200:
                    data = await resp.read()
                    await interaction.followup.send(
                        title + explanation,
                        file=nextcord.File(io.BytesIO(data), "image.png"),
                    )
                    return

        await interaction.followup.send(title + explanation)
        await interaction.channel.send(image.url)

    @nextcord.slash_command(
        "whatsfordinner",
        description="Dad will tell you what to make for dinner based on pictures of your kitchen and ingredients.",
    )
    async def whatsfordinner(
        self,
        interaction: Interaction,
        kitchen: Optional[nextcord.Attachment] = SlashOption(
            description="A picture of your kitchen", required=True
        ),
        ingredients: Optional[nextcord.Attachment] = SlashOption(
            description="A picture of the ingredients you have to work with (like the inside of your fridge)",
            required=True,
        ),
        extra_info: Optional[str] = SlashOption(
            description="Any extra info to tell me about what you want for dinner",
            required=False,
            default="This is my kitchen and ingredients. I want to make something for dinner with these ingredients.",
        ),
    ):
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
        chatCompletion = self.client.chat.completions.create(
            model="gpt-5",
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

        messages = chat_split(response)

        for message in messages:
            await thread.send(message)

    # @nextcord.message_command(name="roastmycode")
    # async def roastmycode(
    #     self, interaction: Interaction, source_message: nextcord.Message
    # ):
    #     """
    #     Have dad roast your code
    #     """
    #     await interaction.response.defer()

    #     system_prompt = "Your goal is to roast someone's code. You should be mean but constructive and a little funny. It is all in good fun but you should make actually good suggestions to improve the code."

    #     await interaction.followup.send("*Your code is bad and you should feel bad*")

    #     await dadroid_single(
    #         system_prompt,
    #         source_message.clean_content,
    #         source_message.reply,
    #         interaction.channel.send,
    #     )

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
            response = "## Writing Onion article!"

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
                name="Onion Article",
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

        messages = chat_split(article_response)

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
                name="Monkey's Paw",
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

        messages = chat_split(article_response)

        for message in messages:
            await thread.send(message)

    @nextcord.slash_command(
        name="summarize_pdf",
        description="Summarize a PDF",
        guild_ids=[850473081063211048],
    )
    async def summarize_pdf(
        self,
        interaction: Interaction,
        pdf: Optional[nextcord.Attachment] = SlashOption(
            description="The PDF to read and summarize", required=True
        ),
    ):
        await interaction.response.defer()
        await pdf.save("temp.pdf")

        try:
            text = extract_text("temp.pdf")
            print(text)
        except Exception as e:
            print(e)

        prompt = f"Summarize the extraction of a PDF that is coming after this. Try to keep the response relatively short, but make sure it's informative.\n\n{text}"

        await dadroid_single(
            "",
            prompt,
            interaction.followup.send,
            interaction.channel.send,
            response_starter="## Here is a summary of the PDF you provided:\n\n",
        )


def setup(bot):
    bot.add_cog(AiStuff(bot))
