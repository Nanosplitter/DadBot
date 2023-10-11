from nextcord import Interaction
from noncommands.chatsplit import chatsplit
import openai
import time

async def dadroid_single(personality, prompt, first_send_method, send_method=None, response_starter=""):
    chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": personality}, {"role": "user", "content": prompt}], stream=True)

    response = response_starter

    

    await respond_from_chat_completion(chatCompletion, first_send_method, send_method, response)

async def dadroid_multiple(personality, messages, first_send_method, send_method, beef = False):
    model = "gpt-3.5-turbo"

    if beef:
        model = "gpt-4"

    chatCompletion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": personality}] + messages, stream=True)

    await respond_from_chat_completion(chatCompletion, first_send_method, send_method)

async def respond_from_chat_completion(chatCompletion, first_send_method, send_method, response = ""):

    if send_method == None:
        send_method = first_send_method

    firstMessage = True

    discord_messages = []

    totalChunks = 0
    last_time_sent =  time.time_ns() // 1_000_000

    for chunk in chatCompletion:
        if not chunk.choices[0].finish_reason == "stop":
            response += chunk.choices[0].delta.content
        
        if last_time_sent + 100 <= (time.time_ns() // 1_000_000) or chunk.choices[0].finish_reason == "stop":
            messages = chatsplit(response)

            messagesSent = 0

            for discord_message in discord_messages:
                await discord_message.edit(content=messages[messagesSent])
                messagesSent += 1
            
            if messagesSent < len(messages):
                for message in messages[messagesSent:]:
                    if firstMessage:
                        discord_messages.append(await first_send_method(message))
                        firstMessage = False
                    else:
                        discord_messages.append(await send_method(message))
            
                    
                    messagesSent += 1
            last_time_sent = time.time_ns() // 1_000_000
        totalChunks += 1
