import os
import discord
from discord.ext import commands
import asyncio

# Intents für deinen Bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Bot erstellen
bot = commands.Bot(command_prefix="!", intents=intents)

# Funktion zum Laden der Cogs
async def load_cogs():
    cogs = ["olddb", "control", "alliance"]  # Cogs müssen im Ordner cogs liegen
    for cog in cogs:
        try:
            await bot.load_extension(f"cogs.{cog}")
            print(f"Cog {cog} erfolgreich geladen.")
        except Exception as e:
            print(f"Fehler beim Laden von {cog}: {e}")

# Event wenn Bot bereit ist
@bot.event
async def on_ready():
    print(f"Bot eingeloggt als {bot.user}")
    print("Slash-Commands und Cogs sollten jetzt verfügbar sein.")

# Hauptfunktion für async Start
async def main():
    await load_cogs()
    TOKEN = os.environ.get("BOT_TOKEN")
    if TOKEN is None:
        print("Fehler: BOT_TOKEN nicht als Environment Variable gesetzt!")
        return
    await bot.start(TOKEN)

# asyncio Loop starten
if __name__ == "__main__":
    asyncio.run(main())
