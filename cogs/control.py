import discord
from discord.ext import commands
import aiohttp
import sqlite3

class Control(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_path = "db/alliance.db"  # Passe den Pfad ggf. an

    @commands.slash_command(name="fid_add", description="Füge einen Spieler über FID hinzu")
    async def fid_add(self, ctx, fid: str):
        await ctx.defer()  # Falls die API länger braucht
        player_data = await self.get_player_data(fid)
        if not player_data:
            await ctx.respond(f"Spieler mit FID `{fid}` nicht gefunden.")
            return

        # Daten aus der API
        name = player_data.get("name")
        level = player_data.get("level")
        alliance = player_data.get("alliance", "Keine Allianz")

        # In Datenbank eintragen
        self.add_to_db(fid, name, level, alliance)

        await ctx.respond(f"Spieler `{name}` (Level {level}) aus Allianz `{alliance}` wurde hinzugefügt.")

    async def get_player_data(self, fid: str):
        # Beispiel-API, du musst den richtigen Endpoint prüfen
        url = f"https://wos-api.example.com/player/{fid}"  # experimentelle API
        headers = {
            "Authorization": f"Bearer DEIN_API_KEY"  # Falls API Key benötigt
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as resp:
                    if resp.status != 200:
                        return None
                    return await resp.json()
            except Exception as e:
                print(f"Fehler beim Abrufen der Daten: {e}")
                return None

    def add_to_db(self, fid, name, level, alliance):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS players (
                fid TEXT PRIMARY KEY,
                name TEXT,
                level INTEGER,
                alliance TEXT
            )
        """)
        cursor.execute("""
            INSERT OR REPLACE INTO players(fid, name, level, alliance) VALUES (?, ?, ?, ?)
        """, (fid, name, level, alliance))
        conn.commit()
        conn.close()


# Setup-Funktion fürs Bot-Framework
async def setup(bot):
    bot.add_cog(Control(bot))  # kein await!
