import discord
from discord.ext import commands
import random
import requests

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='joke')
    async def joke(self, ctx):
        """Envoie une blague aléatoire"""
        response = requests.get("https://official-joke-api.appspot.com/random_joke")
        joke = response.json()
        embed = discord.Embed(
            title="Blague",
            description=f"{joke['setup']}\n\n{joke['punchline']}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name='quote')
    async def quote(self, ctx):
        """Envoie une citation inspirante"""
        response = requests.get("https://api.quotable.io/random")
        quote = response.json()
        embed = discord.Embed(
            title="Citation",
            description=f"{quote['content']}\n\n— {quote['author']}",
            color=discord.Color.purple()
        )
        await ctx.send(embed=embed)

    @commands.command(name='fact')
    async def fact(self, ctx):
        """Envoie un fait aléatoire"""
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        fact = response.json()
        embed = discord.Embed(
            title="Fait",
            description=fact['text'],
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)


    @commands.command(name='8ball')
    async def eight_ball(self, ctx, *, question: str):
        """Répond à une question avec une réponse de type 8ball"""
        responses = [
            "C'est certain.", "Sans aucun doute.", "Oui, définitivement.", "Vous pouvez compter dessus.", 
            "Comme je le vois, oui.", "Très probablement.", "Les perspectives sont bonnes.", "Oui.",
            "Les signes pointent vers oui.", "Réessayez.", "Demandez plus tard.", "Mieux vaut ne pas vous le dire maintenant.",
            "Je ne peux pas prédire maintenant.", "Concentrez-vous et demandez encore.", "Ne comptez pas dessus.",
            "Ma réponse est non.", "Mes sources disent non.", "Les perspectives ne sont pas si bonnes.", "Très douteux."
        ]
        embed = discord.Embed(
            title="8ball",
            description=f"Question: {question}\nRéponse: {random.choice(responses)}",
            color=discord.Color.dark_blue()
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
