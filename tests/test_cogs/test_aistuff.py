import pytest
from nextcord.ext import commands
from cogs.aistuff import AiStuff
from unittest.mock import AsyncMock, MagicMock

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

@pytest.mark.asyncio
async def test_dalle_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.dalle(interaction, prompt="A test prompt", style="vivid")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(f"**A test prompt**\n[style: vivid]", file=MagicMock())

def test_beefydalle_command(cog, bot):
    assert cog.beefydalle.name == "beefydalle"
    assert cog.beefydalle.description == "Create a BEEFY DALL-E 3 image."

@pytest.mark.asyncio
async def test_beefydalle_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.beefydalle(interaction, prompt="A test prompt", style="vivid", size="1024x1024", quality="standard")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(f"**A test prompt**\n[style: vivid] [size: 1024x1024] [quality: standard]", file=MagicMock())

def test_dadroid_command(cog, bot):
    assert cog.dadroid.name == "dadroid"
    assert cog.dadroid.description == "Talk to Dad"

@pytest.mark.asyncio
async def test_dadroid_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.dadroid(interaction, prompt="A test prompt", personality="Test personality")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## A test prompt \n\nTest response")

def test_epicrapbattle_command(cog, bot):
    assert cog.epicrapbattle.name == "epicrapbattle"
    assert cog.epicrapbattle.description == "Create an Epic Rap Battle of History."

@pytest.mark.asyncio
async def test_epicrapbattle_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.epicrapbattle(interaction, person1="Person 1", person2="Person 2")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## Epic Rap Battle of History between Person 1 and Person 2 \n\nTest response")

def test_geoteller_command(cog, bot):
    assert cog.geoteller.name == "geoteller"
    assert cog.geoteller.description == "Get some cool information about a place"

@pytest.mark.asyncio
async def test_geoteller_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.geoteller(interaction, place="Test Place")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## Test Place \n\nTest response")

def test_askfiregator_command(cog, bot):
    assert cog.askfiregator.name == "askfiregator"
    assert cog.askfiregator.description == "Ask Fire Gator for a blessing, a prayer, or insight into the future"

@pytest.mark.asyncio
async def test_askfiregator_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.askfiregator(interaction, prompt="Test prompt")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("**<:praise:931175056472698952> The Great and Mighty Fire Gator hears your request for**\n > Test prompt\n\n **and will oblige <:praise:931175056472698952>** \n\nTest response")

def test_closedopinion_command(cog, bot):
    assert cog.closedopinion.name == "closedopinion"
    assert cog.closedopinion.description == "Generate a new closed opinion on programming"

@pytest.mark.asyncio
async def test_closedopinion_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.closedopinion(interaction, subject="Test subject")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("Test response")

def test_persona_command(cog, bot):
    assert cog.persona.name == "persona"
    assert cog.persona.description == "Have dad respond to the channel with a specific persona"

@pytest.mark.asyncio
async def test_persona_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.persona(interaction, persona="Test persona")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("Test response")

def test_newapod_command(cog, bot):
    assert cog.newapod.name == "newapod"
    assert cog.newapod.description == "Create a new APOD based on your own image"

@pytest.mark.asyncio
async def test_newapod_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    image = MagicMock()
    image.url = "http://example.com/image.png"

    await cog.newapod(interaction, image=image)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(embed=MagicMock())

def test_whatsfordinner_command(cog, bot):
    assert cog.whatsfordinner.name == "whatsfordinner"
    assert cog.whatsfordinner.description == "Dad will tell you what to make for dinner based on pictures of your kitchen and ingredients."

@pytest.mark.asyncio
async def test_whatsfordinner_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    kitchen = MagicMock()
    kitchen.url = "http://example.com/kitchen.png"
    ingredients = MagicMock()
    ingredients.url = "http://example.com/ingredients.png"

    await cog.whatsfordinner(interaction, kitchen=kitchen, ingredients=ingredients, extra_info="Test extra info")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## Yes Chef! Let's get cooking!")

def test_onionarticle_command(cog, bot):
    assert cog.onionarticle.name == "onionarticle"
    assert cog.onionarticle.description == "Create an Onion article."

@pytest.mark.asyncio
async def test_onionarticle_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.onionarticle(interaction, topic="Test topic")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## Writing Onion article!\n\nTopic: Test topic")

def test_monkeyspaw_command(cog, bot):
    assert cog.monkeyspaw.name == "monkeyspaw"
    assert cog.monkeyspaw.description == "Create a new monkey's paw story"

@pytest.mark.asyncio
async def test_monkeyspaw_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.monkeyspaw(interaction, wish="Test wish")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("> Test wish\n\n *The paw curls*")

def test_talk_command(cog, bot):
    assert cog.talk.name == "talk"
    assert cog.talk.description == "Get dad to talk with his voice"

@pytest.mark.asyncio
async def test_talk_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    await cog.talk(interaction, prompt="Test prompt")

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with(file=MagicMock())

def test_summarize_pdf_command(cog, bot):
    assert cog.summarize_pdf.name == "summarize_pdf"
    assert cog.summarize_pdf.description == "Summarize a PDF"

@pytest.mark.asyncio
async def test_summarize_pdf_functionality(cog):
    interaction = AsyncMock()
    interaction.user = MagicMock()
    interaction.user.name = "TestUser"
    interaction.user.id = 123456789
    interaction.response.defer = AsyncMock()
    interaction.followup.send = AsyncMock()

    pdf = MagicMock()
    pdf.url = "http://example.com/test.pdf"

    await cog.summarize_pdf(interaction, pdf=pdf)

    interaction.response.defer.assert_called_once()
    interaction.followup.send.assert_called_once_with("## Here is a summary of the PDF you provided:\n\nTest summary")
