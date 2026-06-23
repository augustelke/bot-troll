import os
import discord
from discord.ext import commands
from discord import app_commands

TOKEN = os.getenv("TOKEN")

AUTHORIZED_USER = 1204841036598354010
ROLE_ID = 1518698406330241024

intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(
command_prefix="!",
intents=intents
)

class CommuView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
```
@discord.ui.button(
    label="Je fais partie de la communauté",
    style=discord.ButtonStyle.success,
    custom_id="commu_button"
)
async def commu_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    role = interaction.guild.get_role(ROLE_ID)

    if role:
        await interaction.user.add_roles(role)

    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message(
            "Bravo tu fais partie de la communauté, n'hésite pas à participer et à parler dans ce serveur.",
            ephemeral=True
        )
    else:
        await interaction.response.send_message(
            "Bravo tu as gagné une place parmi nous.",
            ephemeral=True
        )
```

@bot.event
async def on_ready():
try:
await bot.tree.sync()
bot.add_view(CommuView())
print(f"Connecté : {bot.user}")
except Exception as e:
print(e)

@bot.tree.command(
name="commu",
description="Créer le bouton communauté"
)
async def commu(interaction: discord.Interaction):

```
if interaction.user.id != AUTHORIZED_USER:
    return await interaction.response.send_message(
        "❌ Tu n'as pas la permission.",
        ephemeral=True
    )

await interaction.response.send_message(
    "Clique sur le bouton ci-dessous :",
    view=CommuView()
)
```

@bot.tree.command(
name="envoie",
description="Commande réservée"
)
@app_commands.describe(
phrase="Phrase",
intervalle="Intervalle",
nombre="Nombre de répétitions"
)
async def envoie(
interaction: discord.Interaction,
phrase: str,
intervalle: int,
nombre: int
):

```
if interaction.user.id != AUTHORIZED_USER:
    return await interaction.response.send_message(
        "❌ Tu n'as pas la permission.",
        ephemeral=True
    )

await interaction.response.send_message(
    f"Phrase : {phrase}\n"
    f"Intervalle : {intervalle}\n"
    f"Nombre : {nombre}",
    ephemeral=True
)
```

bot.run(TOKEN)
