import os
import discord
from discord.ext import commands
from discord import app_commands
import asyncio

TOKEN = os.getenv("TOKEN")
AUTHORIZED_USER = int(os.getenv("AUTHORIZED_USER", "0"))
ROLE_ID = int(os.getenv("ROLE_ID", "0"))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)


class CommuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Je fais partie de la communauté",
        style=discord.ButtonStyle.success,
        custom_id="commu_button"
    )
    async def commu_button(self, interaction: discord.Interaction, button: discord.ui.Button):

        role = interaction.guild.get_role(ROLE_ID)

        if role:
            try:
                await interaction.user.add_roles(role)
            except Exception as e:
                print("Erreur role:", e)

        if interaction.user.guild_permissions.administrator:
            msg = "Bravo tu fais partie de la communauté, n'hésite pas à participer."
        else:
            msg = "Bravo tu as rejoint la communauté."

        await interaction.response.send_message(msg, ephemeral=True)


@bot.event
async def on_ready():
    bot.add_view(CommuView())
    await bot.tree.sync()
    print(f"Connecté : {bot.user}")


# =========================
# BOUTON COMMU
# =========================
@bot.tree.command(name="sup")
async def sup(interaction: discord.Interaction, utilisateur: discord.Member):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message("⏳ Suppression en cours...", ephemeral=True)

    channel = interaction.channel
    user = utilisateur

    async def runner():
        try:
            deleted = await delete_task(channel, user)

            await interaction.followup.send(
                f"✅ {deleted} messages supprimés de {user.mention}",
                ephemeral=True
            )

        except Exception as e:
            print("Erreur sup:", e)

            await interaction.followup.send(
                "❌ Erreur pendant la suppression",
                ephemeral=True
            )

    task = asyncio.create_task(runner())

bot.run(TOKEN)
