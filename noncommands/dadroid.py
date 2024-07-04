from typing import Callable, List, Optional
from nextcord import Interaction
from openai import OpenAI, chat
from anthropic import Anthropic
import yaml
from noncommands.chatsplit import chat_split
import base64

# Type aliases for readability
SendMethod = Callable[[str], None]

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


async def dadroid_single(
    personality: str,
    prompt: str,
    first_send_method: SendMethod,
    send_method: Optional[SendMethod] = None,
    response_starter: str = "",
    chats: List[dict] = [],
    beef: bool = False,
) -> None:
    """Handles single message interaction with the chat model."""
    messages = (
        chats
        if chats
        else [
            {"role": "system", "content": personality},
            {"role": "user", "content": prompt},
        ]
    )

    chat_completion = create_chat_completion(messages, beef=beef)
    await respond_from_chat_completion(
        chat_completion, first_send_method, send_method, response_starter
    )


async def dadroid_response(
    personality: str,
    response: str,
    chats: List[dict] = [],
    beef: bool = False,
) -> None:
    """Handles single message interaction with the chat model."""
    messages = (
        chats
        if chats
        else [
            {"role": "system", "content": personality},
            {"role": "user", "content": response},
        ]
    )

    chat_completion = create_chat_completion(messages, beef=beef)

    return chat_completion.choices[0].message.content


async def dadroid_multiple(
    personality: str,
    messages: List[dict],
    first_send_method: SendMethod,
    send_method: SendMethod,
    response_starter: str = "",
) -> None:
    """Handles multiple messages interaction with the chat model."""
    model = "claude-3-5-sonnet-20240620"

    chat_completion = create_chat_completion(messages, model, personality)
    await respond_from_chat_completion(
        chat_completion, first_send_method, send_method, response_starter
    )


def create_chat_completion(
    messages: List[dict], model: str = "claude-3-haiku-20240307", system: str = None
) -> dict:
    """Creates a chat completion using Anthropic's API."""

    client = Anthropic(api_key=config["anthropic_api_key"])

    if system:
        return client.messages.create(
            model=model,
            messages=messages,
            stream=False,
            system=system,
            max_tokens=4096,
        )
    else:
        return client.messages.create(
            model=model,
            messages=messages,
            stream=False,
            max_tokens=4096,
        )


async def respond_from_chat_completion(
    chat_completion: dict,
    first_send_method: SendMethod,
    send_method: Optional[SendMethod],
    initial_response: str = "",
) -> None:
    """Sends response from chat completion."""
    send_method = send_method or first_send_method
    print(chat_completion)
    print(chat_completion.content)
    print(chat_completion.content[0])
    print(chat_completion.content[0].text)
    print(initial_response)
    messages = chat_split(initial_response + chat_completion.content[0].text)

    for index, message in enumerate(messages):
        await (first_send_method if index == 0 else send_method)(message)
