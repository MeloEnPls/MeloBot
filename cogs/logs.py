# cogs/logs.py
import discord
from discord.ext import commands
from discord import AuditLogAction
import config, db

COLOR_MAP = {
    "message_sent": discord.Color.green(),
    # … etc …
    "goulag": discord.Color.dark_red(),
}

class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def log_event(self, event_type: str,
                        agent: discord.abc.User,
                        subject: discord.abc.Snowflake | None,
                        description: str):
        # stocke en BDD
        subj_id = getattr(subject, "id", None)
        await db.add_log(event_type, agent.id, subj_id, description)

        # embed Discord
        chan = self.bot.get_channel(config.LOG_CHANNEL_ID)
        embed = discord.Embed(
            title=event_type.replace("_", " ").title(),
            description=description,
            color=COLOR_MAP.get(event_type, discord.Color.dark_grey())
        )
        embed.set_author(name=str(agent), icon_url=agent.display_avatar.url)
        if subject:
            embed.add_field(name="Sujet", value=subject.mention, inline=True)
        await chan.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot: return
        await self.log_event("message_sent", message.author, message.author, message.content)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        if message.author.bot: return
        # on cherche dans l’audit qui a supprimé
        deleter = None
        async for e in message.guild.audit_logs(limit=5, action=AuditLogAction.message_delete):
            if e.target.id == message.author.id:
                deleter = e.user; break
        agent = deleter or message.author
        desc = f"« {message.content or '<non dispon>'} »"
        await self.log_event("message_deleted", agent, message.author, desc)

    # … et tous tes autres listeners …

async def setup(bot):
    await bot.add_cog(Logs(bot))
