from collections import defaultdict
import re
import yaml
import sys
import os
import mysql.connector
import random
from models.caught import Caught


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class ImChecker:
    def __init__(self):
        self.imList = [
            " im ",
            " i'm ",
            " Im ",
            " I'm ",
            " IM ",
            " I'M ",
            " i am ",
            " I am ",
            " I AM ",
            " lm ",
            " l'm ",
            " lM ",
            " l'M ",
            " l am ",
            " l AM ",
        ]
        self.confusables = Confusables("./resources/likeness.txt")
        self.table = "caught"

    async def checkIm(self, message):
        for string in self.imList:
            confusables_pattern = self.confusables.confusables_regex(string)
            r = re.compile(confusables_pattern)
            fake_string = " " + message.content
            res = r.match(fake_string)
            rand = random.randint(0, 9)

            if res and rand == 3:
                typeIm = res.group().strip() + " "
                await message.reply(
                    f"Hi {message.content.split(typeIm, 1)[1]}, I'm Dad"
                )

                caught_user, _ = Caught.get_or_create(
                    user_id=message.author.id,
                    defaults={"user": str(message.author), "count": 0},
                )
                caught_user.count += 1
                caught_user.save()

                break


class Confusables:
    def __init__(self, confusables_filename):
        f = open(confusables_filename, "r", encoding="utf-8")
        confusables_dict = defaultdict(list)
        pattern = re.compile(r"(.) → (.)")
        for line in f:
            r = pattern.search(line)
            if r:
                fake = r.group(1)
                auth = r.group(2)
                confusables_dict[auth].append(fake)
        self.confusables_dict = confusables_dict

    def expand_char_to_confusables(self, c):
        if c in self.confusables_dict:
            return "[{}{}]".format(
                re.escape(c), re.escape("".join(self.confusables_dict[c]))
            )
        else:
            return c

    def confusables_regex(self, pattern, letter_test_function=None):
        new = ""
        for c in pattern:
            if (not letter_test_function) or (
                letter_test_function and letter_test_function(c)
            ):
                new += self.expand_char_to_confusables(c)
            else:
                new += c
        return new
