import discord
import aiohttp
from discord.ext import commands
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import config, db  # Assure-toi que config.py expose MEMBER_ROLE_ID et WELCOME_CHANNEL_ID

class Welcome(commands.Cog):
    """Cog pour la bannière de bienvenue et l’ajout du rôle membre."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.id != config.GUILD_ID:
            return

        # 0) Ajout du rôle Membre
        member_role = member.guild.get_role(config.MEMBER_ROLE_ID)
        if member_role:
            await member.add_roles(member_role, reason="Rôle Membre automatique")

        # 1) Charge le background
        bg = Image.open("assets/welcome_bg.png").convert("RGBA")

        # 2) Télécharge l’avatar
        async with aiohttp.ClientSession() as sess:
            async with sess.get(str(member.display_avatar.url)) as resp:
                avatar_bytes = await resp.read()
        avatar = Image.open(BytesIO(avatar_bytes)).convert("RGBA").resize((180, 180))

        # 3) Applique un masque circulaire
        mask = Image.new("L", avatar.size, 0)
        ImageDraw.Draw(mask).ellipse((0, 0) + avatar.size, fill=255)
        avatar.putalpha(mask)

        # 4) Colle l’avatar
        bg_w, bg_h = bg.size
        pos = ((bg_w - avatar.width) // 2, 70)
        bg.paste(avatar, pos, avatar)

        # 5) Écrit le texte
        draw = ImageDraw.Draw(bg)
        try:
            font = ImageFont.truetype("arial.ttf", size=60)
        except OSError:
            font = ImageFont.load_default()
        text = f"Welcome {member.name}#{member.discriminator}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        draw.text(((bg_w - text_w) // 2, 270), text, font=font, fill=(255, 255, 255, 255))

        # 6) Envoie l’image
        buf = BytesIO()
        bg.save(buf, format="PNG")
        buf.seek(0)
        file = discord.File(fp=buf, filename="welcome.png")
        channel = member.guild.get_channel(config.WELCOME_CHANNEL_ID)
        if channel:
            await channel.send(file=file)
        else:
            print(f"❌ Channel de bienvenue introuvable ({config.WELCOME_CHANNEL_ID})")

        # 7) Log
        desc = f"{member.mention} a rejoint le serveur et a reçu le rôle Membre"
        await db.add_log("member_join", member.id, member.id, desc)
        logs = self.bot.get_cog("Logs")
        if logs:
            await logs.log_event("member_join", member, member, desc)

async def setup(bot: commands.Bot):
    await bot.add_cog(Welcome(bot))
