from collections import defaultdict
import re
import yaml
import sys
import os
import mysql.connector
import random
from nextcord import Thread
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
        
        messages = await thread.history(limit=20).flatten()

        messages.reverse()

        chatMessages = [{"role": "system", "content": "You are DadBot, a discord chatbot to have fun with the people you chat with. Your goal is to match the energy of the people you are talking to and to always go along with the conversation."}]

        for message in messages:
            if message.author == self.bot.user:
                chatMessages.append({"role": "assistant", "content": message.content})
            else:
                chatMessages.append({"role": "user", "content": message.content})
        
        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=chatMessages)

        response = chatCompletion.choices[0].message.content

        messages = chatsplit(response)

        for message in messages:
            await thread.send(message)

        


