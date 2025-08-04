import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
import matplotlib.pyplot as plt
import io
from services import command_log_service
from datetime import datetime, timedelta, timezone
import yaml

with open("config.yaml") as file:
    config = yaml.load(file, Loader=yaml.FullLoader)


class Stats(commands.Cog, name="stats"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="stats", description="View bot usage statistics")
    async def stats(self, interaction: Interaction):
        """Command group for viewing bot statistics"""
        pass

    @stats.subcommand(
        name="channel_activity",
        description="Show activity stats for all channels in this server (last 30 days)",
    )
    async def channel_activity(self, interaction: Interaction):
        """Show activity stats for all public text channels in this server (last 30 days)"""
        await interaction.response.defer()

        if not interaction.guild:
            await interaction.followup.send(
                "This command can only be used in a server!", ephemeral=True
            )
            return

        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)

        public_channels = [
            channel
            for channel in interaction.guild.text_channels
            if channel.permissions_for(interaction.guild.default_role).view_channel
        ]

        channel_stats = []
        for channel in public_channels:
            message_count = 0
            last_message_date = None

            try:
                # Count recent messages and find most recent
                async for message in channel.history(limit=None, after=thirty_days_ago):
                    message_count += 1
                    if not last_message_date or message.created_at > last_message_date:
                        last_message_date = message.created_at

                # If no recent messages, get the last message ever
                if message_count == 0:
                    async for message in channel.history(limit=1):
                        last_message_date = message.created_at
                        break
            except Exception:
                message_count = -1

            channel_stats.append(
                {"channel": channel, "count": message_count, "last": last_message_date}
            )

        min_datetime = datetime.min.replace(tzinfo=timezone.utc)
        active_channels = [stats for stats in channel_stats if stats["count"] > 0]
        inactive_channels = [stats for stats in channel_stats if stats["count"] == 0]

        active_channels.sort(
            key=lambda stats: (stats["count"], stats["last"] or min_datetime),
            reverse=True,
        )
        inactive_channels.sort(
            key=lambda stats: stats["last"] or min_datetime, reverse=True
        )

        message_lines = []

        if active_channels:
            message_lines.append("**Active channels (Last 30 Days)**")
            for stats in active_channels:
                timestamp = int(stats["last"].timestamp()) if stats["last"] else None
                time_format = f"<t:{timestamp}:R>" if timestamp else "No messages"
                message_lines.append(
                    f"{stats['channel'].mention}: {stats['count']} messages, last: {time_format}"
                )

        if inactive_channels:
            if active_channels:
                message_lines.append("")
            message_lines.append("**Inactive channels and date of their last message**")
            for stats in inactive_channels:
                timestamp = int(stats["last"].timestamp()) if stats["last"] else None
                time_format = f"<t:{timestamp}:R>" if timestamp else "No messages ever"
                message_lines.append(f"{stats['channel'].mention}: {time_format}")

        final_message = (
            "\n".join(message_lines)
            if message_lines
            else "No channels found to analyze."
        )
        await interaction.followup.send(final_message)

    @stats.subcommand(name="commands", description="View the most popular commands")
    async def top_commands(
        self,
        interaction: Interaction,
        count: int = SlashOption(
            description="Number of commands to show", required=False, default=10
        ),
    ):
        """View the most popular commands across all servers"""
        await interaction.response.defer()

        top_commands = command_log_service.get_top_commands(limit=count)

        if not top_commands:
            await interaction.followup.send("No command usage data available yet!")
            return

        lines = [f"Top {len(top_commands)} most used commands:"]
        for i, cmd in enumerate(top_commands, 1):
            lines.append(f"{i}. **{cmd['command_name']}** — {cmd['count']} uses")
        message = "\n".join(lines)

        await interaction.followup.send(message)

    @stats.subcommand(
        name="servers", description="View the servers with most bot usage"
    )
    @commands.is_owner()
    async def top_servers(
        self,
        interaction: Interaction,
        count: int = SlashOption(
            description="Number of servers to show", required=False, default=10
        ),
    ):
        """View the servers with the most command usage (bot owner only)"""
        await interaction.response.defer(ephemeral=True)

        top_servers = command_log_service.get_top_servers(limit=count)

        if not top_servers:
            await interaction.followup.send(
                "No server usage data available yet!", ephemeral=True
            )
            return

        # Build a plain text message instead of an embed
        lines = [f"Top {len(top_servers)} most active servers:"]
        for i, server in enumerate(top_servers, 1):
            lines.append(f"{i}. {server['server_name']} — {server['count']} commands")
        message = "\n".join(lines)

        await interaction.followup.send(message, ephemeral=True)

    @stats.subcommand(name="users", description="View the users with most bot usage")
    @commands.is_owner()
    async def top_users(
        self,
        interaction: Interaction,
        count: int = SlashOption(
            description="Number of users to show", required=False, default=10
        ),
    ):
        """View the users with the most command usage (admin only)"""
        await interaction.response.defer()

        top_users = command_log_service.get_top_users(limit=count)

        if not top_users:
            await interaction.followup.send("No user usage data available yet!")
            return

        lines = [f"Top {len(top_users)} most active users:"]
        for i, user in enumerate(top_users, 1):
            lines.append(f"{i}. **{user['user_name']}** — {user['count']} commands")
        message = "\n".join(lines)

        await interaction.followup.send(message)

    @stats.subcommand(name="server", description="View command usage for this server")
    @commands.has_permissions(administrator=True)
    async def server_stats(
        self,
        interaction: Interaction,
        count: int = SlashOption(
            description="Number of commands to show", required=False, default=10
        ),
    ):
        """View the most popular commands in the current server (admin only)"""
        await interaction.response.defer()

        if not interaction.guild:
            await interaction.followup.send(
                "This command can only be used in a server!"
            )
            return

        server_id = str(interaction.guild.id)
        top_commands = command_log_service.get_top_commands_by_server(
            server_id, limit=count
        )

        if not top_commands:
            await interaction.followup.send(
                "No command usage data available for this server yet!"
            )
            return

        # Build a plain text message instead of an embed
        lines = [
            f"Top {len(top_commands)} most used commands in **{interaction.guild.name}**:"
        ]
        for i, cmd in enumerate(top_commands, 1):
            lines.append(f"{i}. **{cmd['command_name']}** — {cmd['count']} uses")
        message = "\n".join(lines)

        await interaction.followup.send(message)

    @stats.subcommand(
        name="graph", description="View a graph of command usage over time"
    )
    @commands.is_owner()
    async def usage_graph(
        self,
        interaction: Interaction,
        days: int = SlashOption(
            description="Number of days to show", required=False, default=30
        ),
    ):
        """Generate a graph of command usage over time (admin only)"""
        await interaction.response.defer()

        usage_data = command_log_service.get_command_usage_over_time(days=days)

        if not usage_data:
            await interaction.followup.send(
                "No command usage data available for graphing yet!"
            )
            return

        plt.figure(figsize=(10, 6))
        plt.style.use("dark_background")

        dates = list(usage_data.keys())
        counts = list(usage_data.values())

        plt.plot(dates, counts, marker="o", linestyle="-", color="#3498db", linewidth=2)
        plt.title(f"Command Usage Over Past {days} Days", fontsize=16)
        plt.xlabel("Date", fontsize=12)
        plt.ylabel("Commands Used", fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Save plot to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        buf.seek(0)

        file = nextcord.File(buf, filename="command_usage.png")
        await interaction.followup.send(
            f"Command usage over the past {days} days:", file=file
        )
        plt.close()


def setup(bot):
    bot.add_cog(Stats(bot))
