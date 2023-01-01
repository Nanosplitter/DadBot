import yaml
import nextcord
from nextcord.ext import commands
from nextcord import Interaction
import akinator

from akinator import (
    CantGoBackAnyFurther,
    AsyncAkinator,
    Answer,
    Theme
)

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

class Akinator(commands.Cog, name="akinator"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="akinator", description="This command lets you play an akinator game")
    async def akinator(self, interaction: Interaction):
        """
        [No Arguments] This is a command that lets you play an akinator game.
        """
        await interaction.response.defer()
        aki = AsyncAkinator(
            theme=Theme.from_str('characters'),
        )
        first_question = await aki.start_game()
        aki_embed = nextcord.Embed(
            title="Akinator",
            description=first_question,
            color=nextcord.Color.blurple()
        )
        aki_embed.set_image("https://en.akinator.com/bundles/elokencesite/images/akinator.png?v94")
        aki_embed.set_footer(text="Sometimes the bot may say 'This interaction failed', just push the button again.")

        #Create the view for the buttons
        view = nextcord.ui.View()
        view.add_item(nextcord.ui.Button(label="Yes", custom_id="yes"))
        view.add_item(nextcord.ui.Button(label="No", custom_id="no"))
        view.add_item(nextcord.ui.Button(label="Don't Know", custom_id="dont_know"))
        view.add_item(nextcord.ui.Button(label="Probably", custom_id="probably"))
        view.add_item(nextcord.ui.Button(label="Probably Not", custom_id="probably_not"))
        view.add_item(nextcord.ui.Button(label="Back", custom_id="back"))
        view.add_item(nextcord.ui.Button(label="Cancel", custom_id="cancel"))

        # Create the callbacks for the buttons
        async def yes_callback(interaction: Interaction):
            answer = await aki.answer(Answer.Yes)
            aki_embed.description = answer
            if aki.progression >= 80:
                await win()
            else:
                await interaction.response.edit_message(embed=aki_embed) 

        async def no_callback(interaction: Interaction):
            answer = await aki.answer(Answer.No)
            aki_embed.description = answer
            if aki.progression >= 80:
                await win()
            else:
                await interaction.response.edit_message(embed=aki_embed)    

        async def dont_know_callback(interaction: Interaction):
            answer = await aki.answer(Answer.Idk)
            aki_embed.description = answer
            if aki.progression >= 80:
                await win()
            else:
                await interaction.response.edit_message(embed=aki_embed)     

        async def probably_callback(interaction: Interaction):
            answer = await aki.answer(Answer.Probably)
            aki_embed.description = answer
            if aki.progression >= 80:
                await win()
            else:
                await interaction.response.edit_message(embed=aki_embed) 
               
        async def probably_not_callback(interaction: Interaction):
            answer = await aki.answer(Answer.ProbablyNot)
            aki_embed.description = answer
            if aki.progression >= 80:
                await win()
            else:
                await interaction.response.edit_message(embed=aki_embed)    

        async def back_callback(interaction: Interaction):
            try:
                question = await aki.back()
                aki_embed.description = question
                await interaction.response.edit_message(embed=aki_embed)
            except CantGoBackAnyFurther:
                await interaction.response.send_message("You can't go back any further!", ephemeral=True) 

        async def cancel_callback(interaction: Interaction):
            await interaction.response.edit_message(content="Game cancelled!", embed=None, view=None)
        
        # Make function to check for win
        async def win():
            if aki.progression >= 80:
                guess = await aki.win()
                win_embed = nextcord.Embed(
                    title="I think I got it!",
                    description = f"**{guess.name}**: {guess.description}"
                )
                win_embed.set_image(url=guess.absolute_picture_path)
                og_message = await interaction.original_message()
                await og_message.edit(embed=win_embed, view=None)
        
        # Add the callbacks to the buttons
        view.children[0].callback = yes_callback
        view.children[1].callback = no_callback
        view.children[2].callback = dont_know_callback
        view.children[3].callback = probably_callback
        view.children[4].callback = probably_not_callback
        view.children[5].callback = back_callback
        view.children[6].callback = cancel_callback

        view.timeout = 10000

        await interaction.followup.send(embed=aki_embed, view=view)

# And then we finally add the cog to the bot so that it can load, unload, reload and use it's content.
def setup(bot):
    bot.add_cog(Akinator(bot))
