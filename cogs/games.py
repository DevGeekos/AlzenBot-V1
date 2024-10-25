import discord
from discord.ext import commands
import random


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='shifumi')
    async def shifumi(self, ctx, choice: str):
        """Jouer à Shifumi (Pierre, Papier, Ciseaux)"""
        rps_choices = ['pierre', 'papier', 'ciseaux']
        bot_choice = random.choice(rps_choices)
        user_choice = choice.lower()

        if user_choice not in rps_choices:
            await ctx.send(embed=discord.Embed(
                title="Erreur",
                description="Choisissez entre `pierre`, `papier`, ou `ciseaux`.",
                color=discord.Color.red()
            ))
            return

        result = None
        if user_choice == bot_choice:
            result = "Égalité!"
        elif (user_choice == 'pierre' and bot_choice == 'ciseaux') or \
             (user_choice == 'papier' and bot_choice == 'pierre') or \
             (user_choice == 'ciseaux' and bot_choice == 'papier'):
            result = "Vous gagnez!"
        else:
            result = "Vous perdez!"

        embed = discord.Embed(
            title="Shifumi",
            description=f"Votre choix: {user_choice}\nChoix du bot: {bot_choice}\nRésultat: {result}",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)

   

def setup(bot):
    bot.add_cog(Games(bot))
