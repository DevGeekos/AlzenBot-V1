import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='aide')
    async def help_command(self, ctx, *, category=None):
        """Affiche le menu d'aide"""
        if category is None:
            embed = discord.Embed(
                title="Menu d'Aide",
                description="Utilisez `a!help [category]` pour obtenir de l'aide sur une catégorie spécifique.",
                color=discord.Color.gold()
            )
            embed.add_field(name="👋 Bienvenue / Au revoir", value="Commandes de bienvenue et d'au revoir", inline=False)
            embed.add_field(name="🔨 Modération", value="Commandes de modération", inline=False)
            embed.add_field(name="ℹ️ Info", value="Commandes d'information", inline=False)
            embed.add_field(name="🎉 Giveaway", value="Commandes de giveaway", inline=False)
            embed.add_field(name="😄 Fun", value="Commandes amusantes", inline=False)
            embed.add_field(name="🎮 Jeux", value="Commandes de jeux", inline=False)
            await ctx.send(embed=embed)
        else:
            category = category.lower()
            if category == 'bienvenue':
                embed = discord.Embed(
                    title="Bienvenue / Au revoir",
                    description="Commandes pour gérer les messages de bienvenue et d'au revoir",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!setwelcome", value="Configurer le canal et le message de bienvenue", inline=False)
                embed.add_field(name="a!setleave", value="Configurer le canal et le message d'au revoir", inline=False)
                embed.add_field(name="a!welcome [membre]", value="Saluer manuellement un membre", inline=False)
                await ctx.send(embed=embed)
            elif category == 'modération':
                embed = discord.Embed(
                    title="Modération",
                    description="Commandes de modération pour gérer le serveur",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!kick [membre]", value="Expulser un membre du serveur", inline=False)
                embed.add_field(name="a!ban [membre]", value="Bannir un membre du serveur", inline=False)
                embed.add_field(name="a!mute [membre]", value="Muter un membre du serveur", inline=False)
                embed.add_field(name="a!unmute [membre]", value="Démuter un membre du serveur", inline=False)
                embed.add_field(name="a!warn [membre]", value="Avertir un membre du serveur", inline=False)
                embed.add_field(name="a!clear [nombre]", value="Supprimer un nombre spécifié de messages", inline=False)
                await ctx.send(embed=embed)
            elif category == 'info':
                embed = discord.Embed(
                    title="Info",
                    description="Commandes pour obtenir des informations sur le bot, le serveur, les utilisateurs, etc.",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!userinfo [membre]", value="Afficher des informations sur un membre", inline=False)
                embed.add_field(name="a!serverinfo", value="Afficher des informations sur le serveur", inline=False)
                embed.add_field(name="a!channelinfo [channel]", value="Afficher des informations sur un canal", inline=False)
                embed.add_field(name="a!roleinfo [role]", value="Afficher des informations sur un rôle", inline=False)
                embed.add_field(name="a!botinfo", value="Afficher des informations sur le bot", inline=False)
                await ctx.send(embed=embed)
            elif category == 'giveaway':
                embed = discord.Embed(
                    title="Giveaway",
                    description="Commandes pour gérer les giveaways sur le serveur",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!startgiveaway [durée en secondes] [prix]", value="Lancer un giveaway avec une durée et un prix spécifiques", inline=False)
                embed.add_field(name="a!endgiveaway [ID]", value="Terminer un giveaway en cours", inline=False)
                embed.add_field(name="a!rerollgiveaway [ID]", value="Relancer un giveaway pour choisir un nouveau gagnant", inline=False)
                await ctx.send(embed=embed)
            elif category == 'fun':
                embed = discord.Embed(
                    title="Fun",
                    description="Commandes pour s'amuser sur le serveur",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!joke", value="Envoyer une blague aléatoire", inline=False)
                embed.add_field(name="a!quote", value="Envoyer une citation inspirante", inline=False)
                embed.add_field(name="a!fact", value="Envoyer un fait aléatoire", inline=False)
                embed.add_field(name="a!8ball [question]", value="Répondre à une question avec une réponse de type 8ball", inline=False)
                await ctx.send(embed=embed)
            elif category == 'jeux':
                embed = discord.Embed(
                    title="Jeux",
                    description="Commandes de jeux pour jouer sur le serveur",
                    color=discord.Color.gold()
                )
                embed.add_field(name="a!shifumi [choix]", value="Jouer à Shifumi (Pierre, Papier, Ciseaux)", inline=False)
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=discord.Embed(
                    title="Erreur",
                    description="Catégorie invalide.",
                    color=discord.Color.red()
                ))

def setup(bot):
    bot.add_cog(Help(bot))
