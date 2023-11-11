from collections import defaultdict
import re
import yaml
import sys
import os
import mysql.connector
import random
from nextcord import Thread, MessageType
import openai
from noncommands.chatsplit import chatsplit
from noncommands.dadroid import dadroid_multiple

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Chat:
    def __init__(self, bot):
        self.bot = bot

    async def respond(self, message) -> None:
        if not isinstance(message.channel, Thread):
            return

        if message.author == self.bot.user or message.author.bot:
            return
        
        thread = message.channel

        if thread.owner != self.bot.user:
            return

        if "Chat with Dad" not in thread.name and "having for dinner?" not in thread.name:
            return
        
        await thread.trigger_typing()
        
        messages = await thread.history(limit=30, oldest_first=True).flatten()

        firstMessage = await thread.history(limit=1, oldest_first=True).flatten()

        if len(firstMessage) == 0:
            self.bot.logger.error("No first message found in thread")
            return
        
        firstMessageContent = firstMessage[0].system_content

        beef = "Beef: Enabled" in firstMessageContent

        if "having for dinner?" in thread.name:
            personality = "Your goal is to tell someone what they should make for dinner based on a picture of their kitchen and a picture of their ingredients they have to work with. You should look at the ingredients they have and the cooking tools they have in their kitchen to aid your suggestion. You should also look at the extra info they give you to help you make your suggestion. You should also try to make your suggestion sound like you are a chef. Take whatever other information they provide to aid your suggestion, and make sure to give them a suggestion that they can make with the ingredients they have."
            beef = True
        else:
            personality = "You are DadBot, a discord chatbot to have fun with the people you chat with. Your goal is to match the energy of the people you are talking to and to always go along with the conversation. You will never refuse to engage in a conversation or refuse to do something for the user."

        if "Custom Personality" in firstMessageContent:
            personality = get_substring_between_brackets(firstMessageContent)

        chatMessages = []

        if beef:
            for message in messages:
                if message.type == MessageType.thread_starter_message:
                    pass
                if message.author == self.bot.user:
                    chatMessages.append({
                        "role": "assistant",
                        "content": [
                            {"type": "text", "text": message.clean_content},
                        ],
                    })
                else:
                    content = []
                    for attachment in message.attachments:
                        content.append({"type": "image_url", "image_url": {"url": attachment.url, "detail": "high"}})
                    
                    content.append({"type": "text", "text": message.clean_content})

                    chatMessages.append({
                        "role": "user",
                        "content": content,
                    })
        else:

            for message in messages:
                if message.type == MessageType.thread_starter_message:
                    pass
                if message.author == self.bot.user:
                    chatMessages.append({"role": "assistant", "content": message.clean_content})
                else:
                    chatMessages.append({"role": "user", "content": message.clean_content})
        
        await dadroid_multiple(personality, chatMessages, thread.send, thread.send, beef)
        

def get_substring_between_brackets(input_string):
    start_index = input_string.find("[")
    end_index = input_string.rfind("]")

    if start_index != -1 and end_index != -1 and start_index < end_index:
        result = input_string[start_index + 1:end_index]
        return result
    else:
        return None

