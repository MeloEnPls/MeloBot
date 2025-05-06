# cogs/punishment.py
import discord
from discord import app_commands
from discord.ext import commands
import config, db

class Punishment(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.jail = {}  # user_id → minerai restant

    @app_commands.command(name="goulag", description="🔒 Met un membre en goulag")
    @app_commands.describe(target="Membre", ore="Minerais requis")
    @app_commands.checks.has_permissions(administrator=True)
    async def goulag(self, interaction: discord.Interaction,
                     target: discord.Member, ore: int):
        # … tes vérifs …
        self.jail[target.id] = ore
        await db.add_sanction(target.id, interaction.user.id, ore)
        desc = f"{interaction.user.mention} a mis {target.mention} en goulag ({ore})."
        await self.bot.get_cog("Logs").log_event("goulag", interaction.user, target, desc)
        await interaction.response.send_message("🚨 Sanction appliquée.", ephemeral=True)

    # /mine, /ungoulag, /history en copiant le même pattern…

async def setup(bot):
    await bot.add_cog(Punishment(bot))
