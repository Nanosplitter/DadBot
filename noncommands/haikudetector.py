import re
import yaml
import sys
import os
import syllapy
import random
from noncommands.constants import SETTINGS_HINT
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)



class HaikuDetector:
    async def checkForHaiku(self, message, settings):
        if message.guild and message.guild.id in [
            693254450055348294
        ]:
            return
        
        if settings.get("haiku_detector_enabled") != "True":
            return
        
        text = message.content
        words = text.split()[::-1]
        if len(words) < 3:
            return False
        if len(words) > 17:
            return False
        
        line1 = 5
        line2 = 7
        line3 = 5
        line1words = []
        line2words = []
        line3words = []

        for word in words:
            if (syllapy.count(word) == 0):
                return False
            if line1 > 0:
                line1words.append(word)
                line1 -= syllapy.count(word)
            elif line2 > 0:
                line2words.append(word)
                line2 -= syllapy.count(word)
            elif line3 > 0:
                line3words.append(word)
                line3 -= syllapy.count(word)
            else:
                break

        if line1 == 0 and line2 == 0 and line3 == 0 and len(line1words) + len(line2words) + len(line3words) == len(words) and random.randint(1, 100) <= int(settings.get("haiku_detector_response_chance")):
            await message.channel.send(f"You're a poet!\n\n*{' '.join(line3words[::-1])}\n{' '.join(line2words[::-1])}\n{' '.join(line1words[::-1])}*\n- {message.author.mention}\n{SETTINGS_HINT}")
            return True
        return False
        
        