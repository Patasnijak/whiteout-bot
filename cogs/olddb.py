from discord import app_commands
from discord.ext import commands
import sqlite3

class OldDB(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn_users = sqlite3.connect("db/users.sqlite")
        self.conn_changes = sqlite3.connect("db/changes.sqlite")

    @app_commands.command(name="show_users", description="Zeigt alle Benutzer in der Datenbank")
    async def show_users(self, interaction):
        cursor = self.conn_users.cursor()
        cursor.execute("SELECT fid, nickname, furnace_lv, alliance FROM users LIMIT 20")
        users = cursor.fetchall()
        if not users:
            await interaction.response.send_message("Keine Benutzer gefunden.")
            return

        msg = "\n".join([f"FID: {u[0]}, Name: {u[1]}, Furnace: {u[2]}, Allianz: {u[3]}" for u in users])
        await interaction.response.send_message(f"**Benutzerliste:**\n{msg}")

    @app_commands.command(name="nickname_changes", description="Zeigt letzte Nickname-Änderungen")
    async def nickname_changes(self, interaction):
        cursor = self.conn_changes.cursor()
        cursor.execute("SELECT fid, old_nickname, new_nickname, change_date FROM nickname_changes ORDER BY id DESC LIMIT 10")
        changes = cursor.fetchall()
        if not changes:
            await interaction.response.send_message("Keine Nickname-Änderungen gefunden.")
            return

        msg = "\n".join([f"FID: {c[0]} | {c[1]} → {c[2]} | {c[3]}" for c in changes])
        await interaction.response.send_message(f"**Letzte Nickname-Änderungen:**\n{msg}")

async def setup(bot: commands.Bot):
    await bot.add_cog(OldDB(bot))
