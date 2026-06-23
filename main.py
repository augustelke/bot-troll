import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN")
AUTHORIZED_USER = int(os.getenv("AUTHORIZED_USER", "0"))
ROLE_ID = int(os.getenv("ROLE_ID", "0"))

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

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
            except:
                pass

        if interaction.user.guild_permissions.administrator:
            msg = "Bravo tu fais partie de la communauté, n'hésite pas à participer et à parler dans ce serveur."
        else:
            msg = "Bravo tu as gagné une place parmi nous."

        await interaction.response.send_message(msg, ephemeral=True)


@bot.event
async def on_ready():
    bot.add_view(CommuView())

    try:
        await bot.tree.sync()
        print(f"Connecté : {bot.user}")
    except Exception as e:
        print("Erreur sync:", e)


@bot.tree.command(name="commu", description="Créer le bouton communauté")
async def commu(interaction: discord.Interaction):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message(
        "Clique sur le bouton ci-dessous :",
        view=CommuView()
    )


@bot.tree.command(name="envoie", description="Commande admin")
@app_commands.describe(
    phrase="Message",
    intervalle="Intervalle en secondes",
    nombre="Nombre de fois"
)
async def envoie(interaction: discord.Interaction, phrase: str, intervalle: int, nombre: int):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message(
        f"Reçu : {nombre} fois / {intervalle}s / {phrase}",
        ephemeral=True
    )


bot.run(TOKEN)
