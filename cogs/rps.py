import asyncio
import os
import random
import sys
import nextcord
import yaml
from nextcord.ext import commands

if "DadBot" not in str(os.getcwd()):
    os.chdir("./DadBot")
with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# Here we name the cog and create a new class for the cog.
class RPS(commands.Cog, name="rps"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="rps")
    async def rock_paper_scissors(self, context):
        """
        Play a round of Rock-Paper-Scissors with Dad.
        """
        reactions = {
            "🪨": 0,
            "🧻": 1,
            "✂": 2
        }

        embed = nextcord.Embed(title="Please choose", color=config["warning"])
        embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)
        choose_message = await context.send(embed=embed)
        for emoji in reactions:
            await choose_message.add_reaction(emoji)

        def check(reaction, user):
            return user == context.message.author and str(reaction) in reactions

        try:
            reaction, user = await self.bot.wait_for("reaction_add", timeout=10, check=check)

            user_choice_emote = reaction.emoji
            user_choice_index = reactions[user_choice_emote]

            bot_choice_emote = random.choice(list(reactions.keys()))
            bot_choice_index = reactions[bot_choice_emote]

            result_embed = nextcord.Embed(color=config["success"])
            result_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)
            await choose_message.clear_reactions()

            if user_choice_index == bot_choice_index:
                result_embed.description = f"**That's a draw!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["warning"]
            elif user_choice_index == 0 and bot_choice_index == 2:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 1 and bot_choice_index == 0:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            elif user_choice_index == 2 and bot_choice_index == 1:
                result_embed.description = f"**You won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["success"]
            else:
                result_embed.description = f"**I won!**\nYou've chosen {user_choice_emote} and I've chosen {bot_choice_emote}."
                result_embed.colour = config["error"]
                await choose_message.add_reaction("🇱")
            await choose_message.edit(embed=result_embed)
            
        except asyncio.exceptions.TimeoutError:
            await choose_message.clear_reactions()
            timeout_embed = nextcord.Embed(title="Too late", color=config["error"])
            timeout_embed.set_author(name=context.author.display_name, icon_url=context.author.avatar.url)
            await choose_message.edit(embed=timeout_embed)


# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(RPS(bot))
