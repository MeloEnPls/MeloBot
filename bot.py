# bot.py
import discord
from discord.ext import commands
import config, db  # db.py peut rester vide ou ne contenir que init_db()

intents = discord.Intents.default()
# pas de privileged intents nécessaires pour hello/ping

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Connecté comme {bot.user} (ID : {bot.user.id})")

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.core")

    guild = discord.Object(id=config.GUILD_ID)
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)

    print("✅ Cog `core` chargé et slash-commands syncées")

if __name__ == "__main__":
    bot.run(config.TOKEN)
