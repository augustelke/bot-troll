if (interaction.isButton()) {

    if (interaction.customId === "join_community") {

        const member = interaction.member;

        if (member.permissions.has(PermissionFlagsBits.Administrator)) {

            return interaction.reply({
                content:
                    "Bravo tu fais partie de la communauté. N'hésite pas à participer et à parler dans ce serveur.",
                ephemeral: true
            });
        }

        const role = interaction.guild.roles.cache.get(
            "1518698406330241024"
        );

        if (role) {
            await member.roles.add(role);
        }

        return interaction.reply({
            content: "Bravo tu as gagné une place parmi nous.",
            ephemeral: true
        });
    }
}
