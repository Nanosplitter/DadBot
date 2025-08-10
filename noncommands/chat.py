import re
import yaml
from nextcord import Thread, MessageType
from noncommands.chatsplit import chat_split
from pdfminer.high_level import extract_text
import openai
import asyncio

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
        # await thread.trigger_typing()

        messages = [msg async for msg in thread.history(oldest_first=True)]
        first_message = await self.get_first_message(thread)
        if not first_message:
            return

        personality, model = self.determine_personality(
            thread, first_message.system_content
        )

        chat_messages, hasImages = await self.prepare_chat_messages(messages)

        client = openai.AsyncOpenAI(api_key=config["openapi_token"])

        supported_tools = {
            "o3": [],
            "gpt-5-mini": [{"type": "web_search_preview"}],
            "gpt-5": [{"type": "web_search_preview"}],
        }

        # Stream the response and progressively edit a Discord message
        async with thread.typing():
            # Don't send a placeholder; wait for first content
            current_msg = None
            buffer = ""
            last_edit_time = asyncio.get_event_loop().time()
            last_edited_len = 0

            try:
                async with client.responses.stream(
                    model=model,
                    tools=supported_tools.get(model, []),
                    instructions=personality,
                    input=chat_messages,
                    text={"format": {"type": "text"}, "verbosity": "low"},
                ) as stream:
                    edit_interval = 1.0
                    min_delta_chars = 120

                    async for event in stream:
                        if event.type == "response.output_text.delta":
                            buffer += event.delta

                            now = asyncio.get_event_loop().time()

                            if len(buffer) >= 1800:
                                chunks = list(chat_split(buffer))
                                if chunks:
                                    if current_msg is None:
                                        current_msg = await thread.send(
                                            chunks[0], suppress_embeds=True
                                        )
                                    else:
                                        await current_msg.edit(
                                            content=chunks[0], suppress=True
                                        )
                                    for chunk in chunks[1:]:
                                        current_msg = await thread.send(
                                            chunk, suppress_embeds=True
                                        )
                                    buffer = chunks[-1]
                                    last_edit_time = now
                                    last_edited_len = len(buffer)
                            elif (
                                now - last_edit_time >= edit_interval
                                and (len(buffer) - last_edited_len) >= min_delta_chars
                            ) or (len(buffer) - last_edited_len) >= 400:
                                if current_msg is None:
                                    current_msg = await thread.send(
                                        buffer, suppress_embeds=True
                                    )
                                else:
                                    await current_msg.edit(
                                        content=buffer, suppress=True
                                    )
                                last_edit_time = now
                                last_edited_len = len(buffer)
                    if buffer:
                        if current_msg is None:
                            await thread.send(buffer, suppress_embeds=True)
                        else:
                            await current_msg.edit(content=buffer, suppress=True)

            except Exception:
                self.bot.logger.exception(
                    "Streaming failed; falling back to non-streaming."
                )
                try:
                    response = await client.responses.create(
                        model=model,
                        tools=supported_tools.get(model, []),
                        instructions=personality,
                        input=chat_messages,
                        text={"format": {"type": "text"}, "verbosity": "low"},
                    )
                    chunks = list(chat_split(response.output_text))
                    if chunks:
                        if current_msg is None:
                            current_msg = await thread.send(
                                chunks[0], suppress_embeds=True
                            )
                        else:
                            await current_msg.edit(content=chunks[0], suppress=True)
                        for chunk in chunks[1:]:
                            await thread.send(chunk, suppress_embeds=True)
                except Exception:
                    if current_msg is None:
                        await thread.send(
                            "Sorry, I couldn't generate a response.",
                            suppress_embeds=True,
                        )
                    else:
                        await current_msg.edit(
                            content="Sorry, I couldn't generate a response.",
                            suppress=True,
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
        return match.group(1) if match else "gpt-5"  # Default to gpt-5

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
                except Exception:
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
