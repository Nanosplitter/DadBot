import nextcord
from nextcord.ext import bot

@bot.slash_command()
async def echo(interaction: nextcord.Interaction, arg: str):
    """Repeats your message that you send as an argument

    Parameters
    ----------
    interaction: Interaction
        The interaction object
    arg: str
        The message to repeat. This is a required argument.
    """
    await interaction.response.send_message(f"You said: {arg}")