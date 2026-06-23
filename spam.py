import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import time

AUTHORIZED_USER = 1204841036598354010

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.default()
)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Connecté : {bot.user}")

@bot.tree.command(name="envoie", description="Répéter une phrase")
@app_commands.describe(
    phrase="Texte",
    intervalle="Intervalle en secondes",
    nombre="Nombre de répétitions"
)
async def envoie(
    interaction: discord.Interaction,
    phrase: str,
    intervalle: int,
    nombre: int
):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message(
            "❌ Tu n'as pas la permission.",
            ephemeral=True
        )

    await interaction.response.send_message(
        f"✅ Tâche lancée : {nombre} répétitions.",
        ephemeral=True
    )

    for _ in range(nombre):
        print(phrase)
        await asyncio.sleep(intervalle)
