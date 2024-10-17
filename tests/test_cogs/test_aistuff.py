import pytest
from nextcord.ext import commands
from cogs.aistuff import AiStuff

@pytest.fixture
def bot():
    bot = commands.Bot(command_prefix="!")
    return bot

@pytest.fixture
def cog(bot):
    cog = AiStuff(bot)
    bot.add_cog(cog)
    return cog

def test_dalle_command(cog, bot):
    assert cog.dalle.name == "dalle"
    assert cog.dalle.description == "Create a DALL-E 3 image."

def test_beefydalle_command(cog, bot):
    assert cog.beefydalle.name == "beefydalle"
    assert cog.beefydalle.description == "Create a BEEFY DALL-E 3 image."

def test_dadroid_command(cog, bot):
    assert cog.dadroid.name == "dadroid"
    assert cog.dadroid.description == "Talk to Dad"

def test_epicrapbattle_command(cog, bot):
    assert cog.epicrapbattle.name == "epicrapbattle"
    assert cog.epicrapbattle.description == "Create an Epic Rap Battle of History."

def test_geoteller_command(cog, bot):
    assert cog.geoteller.name == "geoteller"
    assert cog.geoteller.description == "Get some cool information about a place"

def test_askfiregator_command(cog, bot):
    assert cog.askfiregator.name == "askfiregator"
    assert cog.askfiregator.description == "Ask Fire Gator for a blessing, a prayer, or insight into the future"

def test_closedopinion_command(cog, bot):
    assert cog.closedopinion.name == "closedopinion"
    assert cog.closedopinion.description == "Generate a new closed opinion on programming"

def test_persona_command(cog, bot):
    assert cog.persona.name == "persona"
    assert cog.persona.description == "Have dad respond to the channel with a specific persona"

def test_newapod_command(cog, bot):
    assert cog.newapod.name == "newapod"
    assert cog.newapod.description == "Create a new APOD based on your own image"

def test_whatsfordinner_command(cog, bot):
    assert cog.whatsfordinner.name == "whatsfordinner"
    assert cog.whatsfordinner.description == "Dad will tell you what to make for dinner based on pictures of your kitchen and ingredients."

def test_onionarticle_command(cog, bot):
    assert cog.onionarticle.name == "onionarticle"
    assert cog.onionarticle.description == "Create an Onion article."

def test_monkeyspaw_command(cog, bot):
    assert cog.monkeyspaw.name == "monkeyspaw"
    assert cog.monkeyspaw.description == "Create a new monkey's paw story"

def test_talk_command(cog, bot):
    assert cog.talk.name == "talk"
    assert cog.talk.description == "Get dad to talk with his voice"

def test_summarize_pdf_command(cog, bot):
    assert cog.summarize_pdf.name == "summarize_pdf"
    assert cog.summarize_pdf.description == "Summarize a PDF"
