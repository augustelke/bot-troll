const {
    Client,
    GatewayIntentBits,
    Collection,
    REST,
    Routes,
    PermissionFlagsBits
} = require("discord.js");

const commands = require("./commands");

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages
    ]
});

client.commands = new Collection();

for (const command of commands) {
    client.commands.set(command.data.name, command);
}

client.once("ready", async () => {
    console.log(`${client.user.tag} connecté`);

    try {

        const rest = new REST({ version: "10" })
            .setToken(process.env.TOKEN);

        await rest.put(
            Routes.applicationCommands(process.env.CLIENT_ID),
            {
                body: commands.map(cmd => cmd.data.toJSON())
            }
        );

        console.log("Commandes enregistrées");

    } catch (err) {
        console.error(err);
    }
});

client.on("interactionCreate", async interaction => {

    if (interaction.isChatInputCommand()) {

        const command =
            client.commands.get(interaction.commandName);

        if (!command) return;

        try {
            await command.execute(interaction);
        } catch (err) {
            console.error(err);

            if (!interaction.replied) {
                await interaction.reply({
                    content: "Erreur commande.",
                    ephemeral: true
                });
            }
        }
    }

    if (interaction.isButton()) {

        if (interaction.customId === "join_community") {

            const member = interaction.member;

            if (
                member.permissions.has(
                    PermissionFlagsBits.Administrator
                )
            ) {
                return interaction.reply({
                    content:
                        "Bravo tu fais partie de la communauté. N'hésite pas à participer et à parler dans ce serveur.",
                    ephemeral: true
                });
            }

            const role =
                interaction.guild.roles.cache.get(
                    "1518698406330241024"
                );

            if (role) {
                await member.roles.add(role);
            }

            return interaction.reply({
                content:
                    "Bravo tu as gagné une place parmi nous.",
                ephemeral: true
            });
        }
    }
});

client.login(process.env.TOKEN);
