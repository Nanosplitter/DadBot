import re
import yaml
from nextcord import Thread, MessageType
from noncommands.chatsplit import chat_split
from pdfminer.high_level import extract_text
import openai

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Chat:
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    @staticmethod
    def load_config():
        with open("config.yaml") as file:
            return yaml.load(file, Loader=yaml.FullLoader)

    async def respond(self, message) -> None:
        if not self.is_valid_thread(message):
            return

        thread = message.channel
        await thread.trigger_typing()

        messages = [msg async for msg in thread.history(oldest_first=True)]
        first_message = await self.get_first_message(thread)
        if not first_message:
            return

        personality, model = self.determine_personality(
            thread, first_message.system_content
        )

        chat_messages, hasImages = await self.prepare_chat_messages(messages)

        client = openai.OpenAI(api_key=config["openapi_token"])

        supported_tools = {
            "o3": [],
            "gpt-4.1": [{"type": "web_search_preview"}],
            "gpt-4.5-preview": [],
        }

        async with thread.typing():
            response = client.responses.create(
                model=model,
                tools=supported_tools.get(model, []),
                instructions=personality,
                input=chat_messages,
            )

        for message in chat_split(response.output_text):
            await thread.send(message, suppress_embeds=True)

    def is_valid_thread(self, message) -> bool:
        if not isinstance(message.channel, Thread):
            return False

        if message.author == self.bot.user or message.author.bot:
            return False

        thread = message.channel
        if thread.owner != self.bot.user:
            return False

        if (
            "Chat with Dad" not in thread.name
            and "having for dinner?" not in thread.name
        ):
            return False

        return True

    async def get_first_message(self, thread) -> str:
        first_message = [msg async for msg in thread.history(oldest_first=True)]
        if len(first_message) == 0:
            self.bot.logger.error("No first message found in thread")
            return None
        return first_message[0]

    def determine_personality(self, thread, first_message_content):
        personality = None
        model = self.extract_model(first_message_content)

        if "having for dinner?" in thread.name:
            personality = self.config["chef_personality"]
        elif "Custom Personality" in first_message_content:
            personality = (
                self.extract_custom_personality(first_message_content)
                + " You are operating in Discord, feel free to use Discord formatting if you'd like, it is a form of Markdown. Try and avoid mentioning that you are talking on discord unless you are asked."
            )

        return personality, model

    @staticmethod
    def extract_custom_personality(input_string):
        match = re.search(r"\[(.*?)\]", input_string, re.DOTALL)
        return match.group(1) if match else None

    @staticmethod
    def extract_model(input_string):
        """Extract model from first message content"""
        match = re.search(r"Model: \[(.*?)\]", input_string)
        return match.group(1) if match else "gpt-4.1"  # Default to gpt-4.1

    async def prepare_chat_messages(self, messages):
        chat_messages = []
        hasImages = False
        for message in messages:
            if message.type == MessageType.thread_starter_message:
                continue

            if message.attachments:
                hasImages = True

            content = []
            if message.author == self.bot.user:
                role = "assistant"
            else:
                role = "user"
                content.extend(
                    await self.prepare_attachment_content(message.attachments)
                )

            content.append(
                {
                    "type": "input_text" if role == "user" else "output_text",
                    "text": message.clean_content,
                }
            )
            chat_messages.append({"role": role, "content": content})

        return chat_messages, hasImages

    @staticmethod
    async def prepare_attachment_content(attachments):
        content = []
        for attachment in attachments:
            if "image" in attachment.content_type:
                content.append(
                    {
                        "type": "input_image",
                        "image_url": attachment.url,
                        "detail": "high",
                    }
                )
            elif "pdf" in attachment.content_type:
                await attachment.save("temp.pdf")

                try:
                    text = extract_text("temp.pdf")
                    content.append(
                        {
                            "type": "input_text",
                            "text": f"Text of PDF the user uploaded:\n\n {text}",
                        }
                    )
                except Exception as e:
                    print(e)
                    content.append(
                        {
                            "type": "input_text",
                            "text": f"There was an error parsing the user's PDF: {attachment.url}",
                        }
                    )
            else:
                content.append(
                    {
                        "type": "input_text",
                        "text": f"Attachment: {attachment.url}",
                    }
                )

        return content
