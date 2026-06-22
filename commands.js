const {
    SlashCommandBuilder,
    EmbedBuilder,
    ActionRowBuilder,
    ButtonBuilder,
    ButtonStyle
} = require("discord.js");

module.exports = [
{
    data: new SlashCommandBuilder()
        .setName("commu")
        .setDescription("Publier le bouton communauté"),

    async execute(interaction) {

        if (interaction.user.id !== "1204841036598354010") {
            return interaction.reply({
                content: "Tu ne peux pas utiliser cette commande.",
                ephemeral: true
            });
        }

        const embed = new EmbedBuilder()
            .setTitle("🌟 Rejoindre la communauté")
            .setDescription(
                "Clique sur le bouton ci-dessous pour rejoindre la communauté."
            )
            .setColor("Blue");

        const row = new ActionRowBuilder().addComponents(
            new ButtonBuilder()
                .setCustomId("join_community")
                .setLabel("Je fais partie de la communauté")
                .setStyle(ButtonStyle.Success)
        );

        await interaction.reply({
            content: "Message envoyé.",
            ephemeral: true
        });

        await interaction.channel.send({
            embeds: [embed],
            components: [row]
        });
    }
}
];
