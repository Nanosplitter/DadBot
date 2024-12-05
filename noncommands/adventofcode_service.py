from datetime import datetime
from zoneinfo import ZoneInfo

def get_advent_of_code_link(day):
    return f"https://adventofcode.com/2024/day/{day}"

async def create_advent_of_code_messages(channel, day=datetime.now(ZoneInfo('America/New_York')).day):
    link = get_advent_of_code_link(day)
    discussion_message_text = f"# :christmas_tree: Advent of Code 2024 Day {day} :snowflake:\n{link}"
    solution_message_text = f"Solution thread for day {day}"
    
    discussion_message = await channel.send(discussion_message_text)
    solution_message = await channel.send(solution_message_text)
    
    discussion_thread = await discussion_message.create_thread(name=f"AoC day {day} Discussion", auto_archive_duration=1440)
    solution_thread = await solution_message.create_thread(name=f"AoC day {day} Solutions", auto_archive_duration=1440)
    
    await discussion_thread.send("Use this thread to discuss the problem and share ideas! No solution spoilers in this thread please!")
    await solution_thread.send("Use this thread to share your solutions!")

