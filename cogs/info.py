import discord
from discord.ext import commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='userinfo')
    async def userinfo(self, ctx, member: discord.Member):
        embed = discord.Embed(title="User Info", description=f"Information sur {member}", color=0x00ff00)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nom", value=member.display_name, inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(name="Role le plus haut", value=member.top_role, inline=True)
        embed.add_field(name="A rejoint", value=member.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True)
        embed.set_footer(text=f"Compte créé le {member.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name='serverinfo')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        embed = discord.Embed(title="Server Info", description=f"Information sur {guild.name}", color=0x00ff00)
        embed.add_field(name="ID", value=guild.id, inline=True)
        embed.add_field(name="Owner", value=guild.owner, inline=True)
        embed.add_field(name="Members", value=guild.member_count, inline=True)
        embed.add_field(name="Roles", value=len(guild.roles), inline=True)
        embed.add_field(name="Channels", value=len(guild.channels), inline=True)
        embed.add_field(name="Région", value=guild.region, inline=True)
        embed.set_footer(text=f"Serveur créé le {guild.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name='channelinfo')
    async def channelinfo(self, ctx, channel: discord.TextChannel):
        embed = discord.Embed(title="Channel Info", description=f"Information sur {channel.name}", color=0x00ff00)
        embed.add_field(name="ID", value=channel.id, inline=True)
        embed.add_field(name="Category", value=channel.category, inline=True)
        embed.add_field(name="Topic", value=channel.topic or "Aucun", inline=True)
        embed.add_field(name="Position", value=channel.position, inline=True)
        embed.set_footer(text=f"Créé le {channel.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name='roleinfo')
    async def roleinfo(self, ctx, role: discord.Role):
        embed = discord.Embed(title="Role Info", description=f"Information sur {role.name}", color=0x00ff00)
        embed.add_field(name="ID", value=role.id, inline=True)
        embed.add_field(name="Couleur", value=role.color, inline=True)
        embed.add_field(name="Mentionnable", value=role.mentionable, inline=True)
        embed.add_field(name="Membres", value=len(role.members), inline=True)
        embed.set_footer(text=f"Créé le {role.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(embed=embed)

    @commands.command(name='botinfo')
    async def botinfo(self, ctx):
        embed = discord.Embed(title="Bot Info", description=f"Information sur {self.bot.user.name}", color=0x00ff00)
        embed.add_field(name="ID", value=self.bot.user.id, inline=True)
        embed.add_field(name="Serveurs", value=len(self.bot.guilds), inline=True)
        embed.add_field(name="Utilisateurs", value=len(self.bot.users), inline=True)
        embed.set_footer(text=f"Bot créé le {self.bot.user.created_at.strftime('%d/%m/%Y %H:%M:%S')}")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))
