import discord
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(embed=discord.Embed(
            title="Membre banni",
            description=f'{member} a été banni pour {reason}',
            color=discord.Color.red()
        ))

    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(embed=discord.Embed(
            title="Membre expulsé",
            description=f'{member} a été expulsé pour {reason}',
            color=discord.Color.orange()
        ))

    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        if not muted_role:
            muted_role = await ctx.guild.create_role(name='Muted')
            for channel in ctx.guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False)
        await member.add_roles(muted_role)
        await ctx.send(embed=discord.Embed(
            title="Membre réduit au silence",
            description=f'{member} a été réduit au silence.',
            color=discord.Color.greyple()
        ))

    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name='Muted')
        await member.remove_roles(muted_role)
        await ctx.send(embed=discord.Embed(
            title="Membre non réduit au silence",
            description=f'{member} peut à nouveau parler.',
            color=discord.Color.green()
        ))

    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(embed=discord.Embed(
            title="Avertissement",
            description=f'{member.mention} a été averti pour {reason}',
            color=discord.Color.gold()
        ))

    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount)
        await ctx.send(embed=discord.Embed(
            title="Messages supprimés",
            description=f'{amount} messages ont été supprimés.',
            color=discord.Color.blue()
        ), delete_after=5)

def setup(bot):
    bot.add_cog(Moderation(bot))
