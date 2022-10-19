import re
import yaml
import sys
import os
import cmudict
import syllables
import string

cd = cmudict.dict()

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)



class HaikuDetector:

    async def checkForHaiku(self, message):
        text = message.content
        words = text.split()[::-1]
        for word in words:
            pass
            
    
    def getSyllables(self, word):
        word = word.translate(str.maketrans('', '', string.punctuation))
        syls = cd[word.lower()]

        if (len(syls) == 0):
            est = syllables.estimate(word)
            return est
        else:
            sylCount = 0
            for sound in syls[0]:
                if sound[-1].isdigit():
                    sylCount += 1
            return sylCount


        