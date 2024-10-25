import discord
from discord.ext import commands

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server_settings = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = member.guild.id
        if guild_id in self.server_settings and 'welcome_channel' in self.server_settings[guild_id]:
            channel = self.bot.get_channel(self.server_settings[guild_id]['welcome_channel'])
            if channel:
                await channel.send(embed=discord.Embed(
                    title="Bienvenue",
                    description=f"Bienvenue {member.mention} ! {self.server_settings[guild_id]['welcome_message']}",
                    color=discord.Color.green()
                ))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        guild_id = member.guild.id
        if guild_id in self.server_settings and 'leave_channel' in self.server_settings[guild_id]:
            channel = self.bot.get_channel(self.server_settings[guild_id]['leave_channel'])
            if channel:
                await channel.send(embed=discord.Embed(
                    title="Au revoir",
                    description=f"Au revoir {member.mention} ! {self.server_settings[guild_id]['leave_message']}",
                    color=discord.Color.red()
                ))

    @commands.command(name='setwelcome')
    @commands.has_permissions(administrator=True)
    async def set_welcome(self, ctx, channel: discord.TextChannel, *, message):
        guild_id = ctx.guild.id
        if guild_id not in self.server_settings:
            self.server_settings[guild_id] = {}
        self.server_settings[guild_id]['welcome_channel'] = channel.id
        self.server_settings[guild_id]['welcome_message'] = message
        await ctx.send(embed=discord.Embed(
            title="Message de bienvenue défini",
            description=f"Message de bienvenue défini pour {channel.mention}",
            color=discord.Color.blue()
        ))

    @commands.command(name='setleave')
    @commands.has_permissions(administrator=True)
    async def set_leave(self, ctx, channel: discord.TextChannel, *, message):
        guild_id = ctx.guild.id
        if guild_id not in self.server_settings:
            self.server_settings[guild_id] = {}
        self.server_settings[guild_id]['leave_channel'] = channel.id
        self.server_settings[guild_id]['leave_message'] = message
        await ctx.send(embed=discord.Embed(
            title="Message d'au revoir défini",
            description=f"Message d'au revoir défini pour {channel.mention}",
            color=discord.Color.blue()
        ))

    @commands.command(name='welcome')
    async def welcome(self, ctx, member: discord.Member):
        await ctx.send(embed=discord.Embed(
            title="Bienvenue",
            description=f"Bienvenue {member.mention} !",
            color=discord.Color.green()
        ))

def setup(bot):
    bot.add_cog(Welcome(bot))
