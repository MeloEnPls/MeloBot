# cogs/core.py
import discord
from discord import app_commands
from discord.ext import commands

class Core(commands.Cog):
    """Cog pour les commandes basiques."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="hello", description="Répond hello world")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("hello world")

    @app_commands.command(name="ping", description="Affiche la latence")
    async def ping(self, interaction: discord.Interaction):
        latency_ms = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong ! Latence : {latency_ms} ms")

async def setup(bot: commands.Bot):
    """Fonction `setup` obligatoire pour load_extension."""
    await bot.add_cog(Core(bot))
