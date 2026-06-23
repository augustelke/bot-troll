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
@bot.tree.command(name="commu", description="Créer le bouton communauté")
async def commu(interaction: discord.Interaction):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message(
        "Clique sur le bouton ci-dessous :",
        view=CommuView()
    )


# =========================
# ENVOI EN BOUCLE (MODIFIÉ)
# =========================
@bot.tree.command(
    name="sup",
    description="Supprimer les messages d'un utilisateur des dernières 24h"
)
@app_commands.describe(
    utilisateur="Utilisateur dont les messages seront supprimés"
)
async def sup(interaction: discord.Interaction, utilisateur: discord.Member):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.defer(ephemeral=True)

    now = discord.utils.utcnow()
    cutoff = now - discord.timedelta(days=1)

    to_delete = []

    async for message in interaction.channel.history(limit=2000):
        if message.author.id != utilisateur.id:
            continue

        if message.created_at < cutoff:
            continue

        to_delete.append(message)

    deleted = 0

    # 🔥 1) Suppression rapide en masse (max 100 messages)
    try:
        for i in range(0, len(to_delete), 100):
            batch = to_delete[i:i+100]
            await interaction.channel.delete_messages(batch)
            deleted += len(batch)

    except discord.Forbidden:
        # fallback si bulk delete impossible
        for msg in to_delete:
            try:
                await msg.delete()
                deleted += 1
            except:
                pass

    await interaction.followup.send(
        f"✅ {deleted} messages supprimés de {utilisateur.mention}",
        ephemeral=True
    )


bot.run(TOKEN)
