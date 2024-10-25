import discord
from discord.ext import commands

class Add(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.support_guild_id = GUILD_ID  # Remplacez ceci par l'ID de votre serveur support
        self.support_channel_id = SUPPORT_CHANNEL_ID  # Remplacez ceci par l'ID du salon support

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Définir l'ID du salon où l'embed sera envoyé
        channel_id = None  # Remplacez ceci par l'ID du salon souhaité

        # Obtenir le salon par son ID
        channel = guild.get_channel(channel_id)

        # Si le salon n'existe pas, chercher un autre salon texte disponible
        if channel is None:
            for ch in guild.text_channels:
                if ch.permissions_for(guild.me).send_messages:
                    channel = ch
                    break

        # Si un salon est trouvé, envoyer l'embed
        if channel:
            embed = discord.Embed(
                title="Merci de m'avoir ajouté!",
                description="Je suis un bot prêt à vous aider à gérer votre serveur.",
                color=discord.Color.blue()
            )
            embed.add_field(name="Commandes", value="Utilisez `a!aide` pour voir toutes mes commandes disponibles.")
            embed.set_footer(text="Bot développé par orionofficiel")

            await channel.send(embed=embed)
        else:
            print(f"Impossible de trouver un salon pour envoyer le message dans le serveur {guild.name}")

        # Envoyer un message au serveur support
        await self.send_support_message(guild)

    async def send_support_message(self, guild):
        support_guild = self.bot.get_guild(self.support_guild_id)
        if support_guild:
            support_channel = support_guild.get_channel(self.support_channel_id)
            if support_channel:
                embed = discord.Embed(
                    title="Nouveau serveur ajouté!",
                    description=f"Le bot a été ajouté au serveur: **{guild.name}** (ID: {guild.id})",
                    color=discord.Color.green()
                )
                embed.add_field(name="Membres", value=f"{guild.member_count}")
                embed.set_footer(text="Bot Notification")
                await support_channel.send(embed=embed)
            else:
                print(f"Impossible de trouver le salon support avec l'ID {self.support_channel_id}")
        else:
            print(f"Impossible de trouver le serveur support avec l'ID {self.support_guild_id}")

def setup(bot):
    bot.add_cog(Add(bot))
