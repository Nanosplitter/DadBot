from nextcord import Interaction
from noncommands.chatsplit import chatsplit
import openai
import time

async def dadroid_single(personality, prompt, first_send_method, send_method=None, response_starter="", chats = []):
    if len(chats) > 0:
        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=chats, stream=True)
    else:
        chatCompletion = openai.ChatCompletion.create(model="gpt-3.5-turbo-1106", messages=[{"role": "system", "content": personality}, {"role": "user", "content": prompt}], stream=True)

    response = response_starter

    await respond_from_chat_completion(chatCompletion, first_send_method, send_method, response)

async def dadroid_multiple(personality, messages, first_send_method, send_method, beef = False):
    model = "gpt-3.5-turbo-1106"

    try:
        if beef:
            model = "gpt-4-vision-preview"
            chatCompletion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": personality}] + messages, stream=False, max_tokens=1024)
            await respond_from_chat_completion_no_stream(chatCompletion, first_send_method, send_method)
        else:
            chatCompletion = openai.ChatCompletion.create(model=model, messages=[{"role": "system", "content": personality}] + messages, stream=True, max_tokens=1024)
            await respond_from_chat_completion(chatCompletion, first_send_method, send_method)
    except openai.error.APIError:
        await first_send_method("I'm sorry, my system is currently having some issues. Send another message! If that doesn't work, wait a few minutes and try again.")

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


async def respond_from_chat_completion_no_stream(chatCompletion, first_send_method, send_method, response = ""):

    if send_method == None:
        send_method = first_send_method

    messages = chatsplit(chatCompletion.choices[0].message.content)

    firstMessage = True

    for message in messages:
        if firstMessage:
            await first_send_method(message)
            firstMessage = False
            firstMessage = False
        else:
            await send_method(message)

    

