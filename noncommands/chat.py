import re
import yaml
from nextcord import Thread, MessageType
from noncommands.dadroid import dadroid_multiple
import base64


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

        messages = await thread.history(limit=30, oldest_first=False).flatten()
        messages.reverse()
        first_message = await self.get_first_message(thread)
        if not first_message:
            return

        personality = self.determine_personality(
            thread, first_message.system_content
        )

        chat_messages = await self.prepare_chat_messages(messages)

        await dadroid_multiple(
            personality, chat_messages, thread.send, thread.send
        )

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
        first_message = await thread.history(limit=1, oldest_first=True).flatten()
        if len(first_message) == 0:
            self.bot.logger.error("No first message found in thread")
            return None
        return first_message[0]

    def determine_personality(self, thread, first_message_content):
        personality = self.config["default_personality"]

        if "having for dinner?" in thread.name:
            personality = self.config["chef_personality"]
        elif "Custom Personality" in first_message_content:
            personality = (
                self.extract_custom_personality(first_message_content)
                + " You are operating in Discord, feel free to use Discord formatting if you'd like, it is a form of Markdown. Try and avoid mentioning that you are talking on discord unless you are asked."
            )

        return personality

    @staticmethod
    def extract_custom_personality(input_string):
        match = re.search(r"\[(.*?)\]", input_string, re.DOTALL)
        return match.group(1) if match else None

    async def prepare_chat_messages(self, messages):
        chat_messages = []
        for message in messages:
            if message.type == MessageType.thread_starter_message:
                continue

            content = []
            if message.author == self.bot.user:
                role = "assistant"
            else:
                role = "user"
                content.extend(await self.prepare_attachment_content(message.attachments))

            content.append({"type": "text", "text": message.clean_content})
            chat_messages.append({"role": role, "content": content})

        return chat_messages

    @staticmethod
    async def prepare_attachment_content(attachments):
        # Read each attachment and convert it to base64 for the model
        content = []
        for attachment in attachments:
            if attachment.content_type in ["image/png", "image/jpeg", "image/jpg", "image/gif", "image/webp"]:
                content.append(
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": attachment.content_type,
                            "data": base64.b64encode(await attachment.read()).decode("utf-8"),
                        }
                    }
                )
        return content
