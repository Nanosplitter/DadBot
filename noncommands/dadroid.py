from typing import Callable, List, Optional
from openai import OpenAI
import yaml
from noncommands.chatsplit import chat_split

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
    model: str = "gpt-5",
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

    chat_completion = create_chat_completion(messages, model, beef)
    await respond_from_chat_completion(
        chat_completion, first_send_method, send_method, response_starter
    )


async def dadroid_response(
    personality: str,
    response: str,
    chats: List[dict] = [],
    beef: bool = False,
    model: str = "gpt-5",
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

    chat_completion = create_chat_completion(messages, model, beef)

    return chat_completion.choices[0].message.content


async def dadroid_multiple(
    personality: str,
    messages: List[dict],
    first_send_method: SendMethod,
    send_method: SendMethod,
    beef: bool = False,
    response_starter: str = "",
    model: str = "gpt-5",
) -> None:
    """Handles multiple messages interaction with the chat model."""
    # Use the provided model parameter instead of hardcoded logic
    messages_with_personality = [{"role": "system", "content": personality}] + messages

    chat_completion = create_chat_completion(messages_with_personality, model)
    await respond_from_chat_completion(
        chat_completion, first_send_method, send_method, response_starter
    )


def create_chat_completion(
    messages: List[dict], model: str = "gpt-5", beef: bool = False
) -> dict:
    """Creates a chat completion using OpenAI's API."""

    client = OpenAI(api_key=config["openapi_token"])

    # If beef is True and no specific model is provided, use gpt-5
    if beef and model == "gpt-5":
        model = "gpt-5"

    return client.chat.completions.create(model=model, messages=messages, stream=False)


async def respond_from_chat_completion(
    chat_completion: dict,
    first_send_method: SendMethod,
    send_method: Optional[SendMethod],
    initial_response: str = "",
) -> None:
    """Sends response from chat completion."""
    send_method = send_method or first_send_method
    messages = chat_split(initial_response + chat_completion.choices[0].message.content)

    for index, message in enumerate(messages):
        await (first_send_method if index == 0 else send_method)(message)
