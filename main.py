from datetime import timedelta
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

# 🔒 Lock global pour éviter 2 suppressions en même temps
sup_lock = asyncio.Lock()


# =========================
# VIEW COMMU
# =========================
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


# =========================
# READY
# =========================
@bot.event
async def on_ready():
    bot.add_view(CommuView())
    await bot.tree.sync()
    print(f"Connecté : {bot.user}")


# =========================
# COMMU COMMAND
# =========================
@bot.tree.command(name="commu")
async def commu(interaction: discord.Interaction):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message(
        "Clique sur le bouton ci-dessous :",
        view=CommuView()
    )


# =========================
# ENVOI BOUCLE (SAFE)
# =========================
@bot.tree.command(name="envoie")
@app_commands.describe(
    cible="ID salon ou utilisateur",
    phrase="Message",
    intervalle="Temps entre messages",
    nombre="Nombre d'envois"
)
async def envoie(interaction: discord.Interaction, cible: str, phrase: str, intervalle: int, nombre: int):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message("✅ Envoi lancé", ephemeral=True)

    channel = None
    user = None

    try:
        channel = bot.get_channel(int(cible))
    except:
        pass

    if channel is None:
        try:
            user = await bot.fetch_user(int(cible))
        except:
            return await interaction.followup.send("❌ ID invalide", ephemeral=True)

    async def task():
        try:
            for _ in range(nombre):
                if channel:
                    await channel.send(phrase)
                elif user:
                    await user.send(phrase)

                await asyncio.sleep(intervalle)

        except Exception as e:
            print("Erreur envoie:", e)

    asyncio.create_task(task())


# =========================
# FONCTION SUPPRESSION
# =========================
async def delete_task(channel, utilisateur):

    now = discord.utils.utcnow()
    cutoff = now - timedelta(days=1)

    messages = []

    async for msg in channel.history(limit=2000):
        if msg.author.id != utilisateur.id:
            continue
        if msg.created_at < cutoff:
            continue
        messages.append(msg)

    deleted = 0

    # 🔥 bulk delete (rapide)
    for i in range(0, len(messages), 100):
        batch = messages[i:i+100]

        try:
            await channel.delete_messages(batch)
            deleted += len(batch)

        except Exception:
            # fallback safe
            for m in batch:
                try:
                    await m.delete()
                    deleted += 1
                except:
                    pass

    return deleted


# =========================
# SUPPRESSION SAFE
# =========================
@bot.tree.command(name="sup")
async def sup(interaction: discord.Interaction, utilisateur: discord.Member):

    if interaction.user.id != AUTHORIZED_USER:
        return await interaction.response.send_message("❌ Pas autorisé", ephemeral=True)

    await interaction.response.send_message("⏳ Suppression en cours...", ephemeral=True)

    channel = interaction.channel
    user = utilisateur

    async def runner():

        async with sup_lock:
            try:
                deleted = await delete_task(channel, user)

                await interaction.followup.send(
                    f"✅ {deleted} messages supprimés de {user.mention}",
                    ephemeral=True
                )

            except Exception as e:
                print("Erreur sup:", e)

                try:
                    await interaction.followup.send(
                        "❌ Erreur pendant la suppression",
                        ephemeral=True
                    )
                except:
                    pass

    asyncio.create_task(runner())


# =========================
# RUN BOT
# =========================
bot.run(TOKEN)
