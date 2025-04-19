from typing import List


def chat_split(text: str, help=False) -> List[str]:
    chunks: List[str] = []
    split = text.split("```")

    for i in range(len(split)):
        if split[i] == "":
            continue
        if i % 2 == 0:
            if not help:
                processNonCodeBlock(split[i], chunks)
            else:
                processHelpBlock(split[i], chunks)
        else:
            processCodeBlock(split[i], chunks)

    return chunks

def processNonCodeBlock(text: str, chunks: List[str]) -> None:
    while len(text) > 2000:
        index = text[:2000].rfind("\n")
        if index == -1:
            index = 2000
        chunks.append(text[:index])
        text = text[index:]
    chunks.append(text)

def processCodeBlock(text: str, chunks: List[str]) -> None:
    language = text[:text.index("\n")]
    text = text[text.index("\n") + 1:]

    while len(text) > 1990:
        index = text[:1990].rfind("\n")
        if index == -1:
            index = 1990

        chunks.append(f"```{language}\n{text[:index]}```")
        text = text[index:]
    chunks.append(f"```{language}\n{text}```")

def processHelpBlock(text: str, chunks: List[str]) -> None:
    while len(text) > 2000:
        index = text[:2000].rfind("## ")
        if index == 0:
            index = text[:2000].rfind("- **`/")
        if index == -1:
            index = 2000
        chunks.append(text[:index])
        text = text[index:]
    chunks.append(text)

