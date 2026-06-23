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
@bot.tree.command(name="envoie", description="Envoie un message en boucle dans un salon ou DM")
@app_commands.describe(
    cible="ID du salon ou ID utilisateur",
    phrase="Message à envoyer",
    intervalle="Intervalle en secondes",
    nombre="Nombre de fois"
)
async def envoie(
    interaction: discord.Interaction,
    cible: str,
    phrase: str,
    intervalle: int,
    nombre: int
):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message("✅ Envoi lancé", ephemeral=True)

    channel = None
    user = None

    # -------------------------
    # ESSAYE SALON
    # -------------------------
    try:
        channel_id = int(cible)
        channel = bot.get_channel(channel_id)
    except:
        pass

    # -------------------------
    # SI PAS SALON → USER
    # -------------------------
    if channel is None:
        try:
            user_id = int(cible)
            user = await bot.fetch_user(user_id)
        except:
            return await interaction.followup.send("❌ ID invalide", ephemeral=True)

    # -------------------------
    # BOUCLE D'ENVOI
    # -------------------------
    for i in range(nombre):

        try:
            if channel:
                await channel.send(phrase)
            elif user:
                await user.send(phrase)

        except Exception as e:
            print("Erreur envoi:", e)

        await asyncio.sleep(intervalle)

@bot.tree.command(
name="sup",
description="Supprimer les messages d'un utilisateur des dernières 24h"
)
@app_commands.describe(
utilisateur="Utilisateur dont les messages seront supprimés"
)
async def sup(
interaction: discord.Interaction,
utilisateur: discord.Member
):
    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message(
            "❌ Pas autorisé",
            ephemeral=True
        )
    await interaction.response.defer(ephemeral=True)

    deleted = 0
    
    async for message in interaction.channel.history(limit=10000):
        if message.author.id != utilisateur.id:
            continue
    
        age = discord.utils.utcnow() - message.created_at
    
        if age.total_seconds() > 86400:
            continue
    
        try:
            await message.delete()
            deleted += 1
        except Exception:
            pass
    
    await interaction.followup.send(
        f"✅ {deleted} messages supprimés de {utilisateur.mention}",
        ephemeral=True
    )


bot.run(TOKEN)
