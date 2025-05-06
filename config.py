import os
from dotenv import load_dotenv

load_dotenv()
TOKEN              = os.getenv("DISCORD_TOKEN")
GUILD_ID           = int(os.getenv("GUILD_ID", 0))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", 0))
PRISONER_ROLE_ID   = int(os.getenv("PRISONER_ROLE_ID", 0))
MEMBER_ROLE_ID     = int(os.getenv("MEMBER_ROLE_ID", 0))
LOG_CHANNEL_ID     = int(os.getenv("LOG_CHANNEL_ID", 0))

if not all([TOKEN, GUILD_ID, WELCOME_CHANNEL_ID,
            PRISONER_ROLE_ID, MEMBER_ROLE_ID, LOG_CHANNEL_ID]):
    raise RuntimeError("Il manque une variable d'environnement dans .env")
