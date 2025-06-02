import nextcord
import yaml
from nextcord.ext import commands
from nextcord.ui import Button, TextInput
from nextcord import Interaction


with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Poll(commands.Cog, name="poll"):
    def __init__(self, bot):
        self.bot = bot

    class PollBuilder(nextcord.ui.Modal):
        def __init__(self, number_of_boxes, is_default):
            super().__init__("Poll Builder")
            self.number_of_boxes = number_of_boxes
            self.is_default = is_default
            self.text_inputs = []

            question_input = TextInput(
                label="Question", placeholder="Question", max_length=500, required=True
            )
            self.add_item(question_input)

            if not self.is_default:
                for i in range(self.number_of_boxes):
                    text_input = TextInput(
                        label=f"Option {i + 1}",
                        placeholder=f"Option {i + 1}",
                        max_length=500,
                        required=False,
                    )
                    self.text_inputs.append(text_input)
                    self.add_item(text_input)

        async def callback(self, interaction: Interaction):
            await interaction.response.defer()
            values = []
            for item in self.text_inputs:
                value = item.value
                if value == "":
                    value = " "
                values.append(value)

            embed = nextcord.Embed(title=f"{self.children[0].value}")
            for i in range(len(values)):
                embed.add_field(
                    name=f"{i + 1}\N{combining enclosing keycap} - {values[i]}",
                    value="-----------",
                    inline=False,
                )

            member = nextcord.utils.get(
                interaction.guild.members, name=interaction.user.name
            )
            embed.set_author(
                name=f"New Poll from {interaction.user.nick}",
                icon_url=f"{member.display_avatar.url}",
            )
            # embed.set_footer(text=f"Poll made by {interaction.user.nick}", icon_url=member.display_avatar.url)
            embed_message = await interaction.channel.send(embed=embed)

            if self.is_default:
                await embed_message.add_reaction("👍")
                await embed_message.add_reaction("👎")
                await embed_message.add_reaction("🤷")
            else:
                for i in range(len(values)):
                    await embed_message.add_reaction(
                        f"{i + 1}\N{combining enclosing keycap}"
                    )
                await embed_message.add_reaction("🤷")

    @nextcord.slash_command(
        name="poll", description="Create a poll where members can vote."
    )
    async def poll(self, interaction: Interaction):
        """
        [None] Create a poll where members can vote.
        """
        embed = nextcord.Embed(
            title="Time to create a poll!",
            description="Select the number of options you want to have in your poll.",
        )
        embed.add_field(
            name="Custom Poll",
            value="You can customize the options you want to have in your poll.",
            inline=False,
        )
        embed.add_field(
            name="Default Poll",
            value="You will have 3 options in your poll that you don't get to specify. (👍, 👎, 🤷)",
            inline=False,
        )

        view = nextcord.ui.View(timeout=None)

        select_options = [
            nextcord.SelectOption(label="1 Option", value="1"),
            nextcord.SelectOption(label="2 Options", value="2"),
            nextcord.SelectOption(label="3 Options", value="3"),
            nextcord.SelectOption(label="4 Options", value="4"),
        ]

        string_select = nextcord.ui.Select(
            options=select_options,
            placeholder="Number of response options",
            min_values=1,
            max_values=1,
        )

        view.add_item(string_select)

        custom_poll_button = Button(
            label="Custom Poll", style=nextcord.ButtonStyle.green
        )
        default_poll_button = Button(
            label="Default Poll", style=nextcord.ButtonStyle.grey
        )

        async def custom_poll_button_callback(interaction):
            modal = self.PollBuilder(int(string_select.values[0]), False)

            await interaction.response.send_modal(modal)

        async def default_poll_button_callback(interaction):
            modal = self.PollBuilder(3, True)

            await interaction.response.send_modal(modal)

        custom_poll_button.callback = custom_poll_button_callback
        default_poll_button.callback = default_poll_button_callback

        view.add_item(custom_poll_button)
        view.add_item(default_poll_button)

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(Poll(bot))
