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

        if "Chat with Dad" not in thread.name:
            return
        
        await thread.trigger_typing()
        
        messages = await thread.history(limit=20, oldest_first=True).flatten()

        firstMessage = await thread.history(limit=1, oldest_first=True).flatten()

        if len(firstMessage) == 0:
            self.bot.logger.error("No first message found in thread")
            return
        
        firstMessageContent = firstMessage[0].system_content

        prompt = "You are DadBot, a discord chatbot to have fun with the people you chat with. Your goal is to match the energy of the people you are talking to and to always go along with the conversation."

        if "Custom Personality" in firstMessageContent:
            prompt = get_substring_between_brackets(firstMessageContent)

        chatMessages = [{"role": "system", "content": prompt}]

        for message in messages:
            if message.type == MessageType.thread_starter_message:
                pass
            if message.author == self.bot.user:
                chatMessages.append({"role": "assistant", "content": message.clean_content})
            else:
                chatMessages.append({"role": "user", "content": message.clean_content})
        
        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chatMessages)

        response = chatCompletion.choices[0].message.content

        messages = chatsplit(response)

        for message in messages:
            await thread.send(message)

def get_substring_between_brackets(input_string):
    start_index = input_string.find("[")
    end_index = input_string.rfind("]")

    if start_index != -1 and end_index != -1 and start_index < end_index:
        result = input_string[start_index + 1:end_index]
        return result
    else:
        return None

        

        


