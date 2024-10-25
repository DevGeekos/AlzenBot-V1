import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta
import pytz

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaways = {}

    @commands.command(name='startgiveaway')
    @commands.has_permissions(administrator=True)
    async def start_giveaway(self, ctx, duration: int, *, prize: str):
        """Lance un giveaway"""
        # Set the timezone to the desired timezone, e.g., UTC or local timezone
        timezone = pytz.timezone('Europe/Paris')
        
        # Get the current time in the desired timezone
        now = datetime.now(timezone)
        
        # Calculate the end time
        end_time = now + timedelta(seconds=duration)
        
        # Create the giveaway message
        giveaway_message = await ctx.send(embed=discord.Embed(
            title="🎉 Giveaway ! 🎉",
            description=f"Prix: **{prize}**\nRéagissez avec 🎉 pour participer!\nSe termine <t:{int(end_time.timestamp())}:R>",
            color=discord.Color.blue()
        ))
        await giveaway_message.add_reaction("🎉")

        # Store the giveaway information
        self.giveaways[giveaway_message.id] = {
            "channel": ctx.channel.id,
            "end_time": end_time,
            "prize": prize,
            "message_id": giveaway_message.id
        }

        # Wait for the duration of the giveaway
        await asyncio.sleep(duration)

        # End the giveaway if it is still active
        if giveaway_message.id in self.giveaways:
            await self.end_giveaway(giveaway_message.id)

    @commands.command(name='endgiveaway')
    @commands.has_permissions(administrator=True)
    async def end_giveaway_command(self, ctx, message_id: int):
        """Termine un giveaway manuellement"""
        if message_id in self.giveaways:
            await self.end_giveaway(message_id)
        else:
            await ctx.send("Aucun giveaway trouvé avec cet ID.")

    async def end_giveaway(self, message_id):
        giveaway = self.giveaways.pop(message_id)
        channel = self.bot.get_channel(giveaway["channel"])
        message = await channel.fetch_message(giveaway["message_id"])
        users = await message.reactions[0].users().flatten()
        users = [user for user in users if not user.bot]

        if users:
            winner = random.choice(users)
            await channel.send(embed=discord.Embed(
                title="🎉 Giveaway terminé ! 🎉",
                description=f"Félicitations {winner.mention}, vous avez gagné **{giveaway['prize']}**!",
                color=discord.Color.green()
            ))
        else:
            await channel.send(embed=discord.Embed(
                title="🎉 Giveaway terminé ! 🎉",
                description="Aucun participant, aucun gagnant.",
                color=discord.Color.red()
            ))

    @commands.command(name='rerollgiveaway')
    @commands.has_permissions(administrator=True)
    async def reroll_giveaway(self, ctx, message_id: int):
        """Relance un giveaway pour choisir un nouveau gagnant"""
        if message_id not in self.giveaways:
            await ctx.send("Aucun giveaway trouvé avec cet ID.")
            return

        giveaway = self.giveaways[message_id]
        channel = self.bot.get_channel(giveaway["channel"])
        message = await channel.fetch_message(giveaway["message_id"])
        users = await message.reactions[0].users().flatten()
        users = [user for user in users if not user.bot]

        if users:
            winner = random.choice(users)
            await channel.send(embed=discord.Embed(
                title="🎉 Giveaway relancé ! 🎉",
                description=f"Félicitations {winner.mention}, vous avez gagné **{giveaway['prize']}**!",
                color=discord.Color.green()
            ))
        else:
            await channel.send(embed=discord.Embed(
                title="🎉 Giveaway relancé ! 🎉",
                description="Aucun participant, aucun gagnant.",
                color=discord.Color.red()
            ))

def setup(bot):
    bot.add_cog(Giveaway(bot))
