import discord
from discord.ext import commands
import json
import os
from collections import defaultdict, deque
from datetime import datetime, timedelta

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.automod_config = {}
        self.load_config()
        self.message_history = defaultdict(lambda: defaultdict(deque))
        self.mention_history = defaultdict(lambda: defaultdict(deque))

    def load_config(self):
        if os.path.exists('automod_config.json'):
            with open('automod_config.json', 'r') as f:
                self.automod_config = json.load(f)
        else:
            self.automod_config = {}

    def save_config(self):
        with open('automod_config.json', 'w') as f:
            json.dump(self.automod_config, f, indent=4)

    @commands.command(name='addbadword')
    @commands.has_permissions(manage_messages=True)
    async def add_bad_word(self, ctx, *, word: str):
        """Ajouter un mot à la liste des mots interdits pour ce serveur"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.automod_config:
            self.automod_config[guild_id] = {"bad_words": [], "spam_threshold": 5, "spam_interval": 10, "mention_threshold": 5, "mention_interval": 10}

        if word.lower() not in self.automod_config[guild_id]["bad_words"]:
            self.automod_config[guild_id]["bad_words"].append(word.lower())
            self.save_config()
            await ctx.send(f"Le mot `{word}` a été ajouté à la liste des mots interdits pour ce serveur.")
        else:
            await ctx.send(f"Le mot `{word}` est déjà dans la liste des mots interdits pour ce serveur.")

    @commands.command(name='removebadword')
    @commands.has_permissions(manage_messages=True)
    async def remove_bad_word(self, ctx, *, word: str):
        """Supprimer un mot de la liste des mots interdits pour ce serveur"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.automod_config and word.lower() in self.automod_config[guild_id]["bad_words"]:
            self.automod_config[guild_id]["bad_words"].remove(word.lower())
            self.save_config()
            await ctx.send(f"Le mot `{word}` a été supprimé de la liste des mots interdits pour ce serveur.")
        else:
            await ctx.send(f"Le mot `{word}` n'est pas dans la liste des mots interdits pour ce serveur.")

    @commands.command(name='listbadwords')
    @commands.has_permissions(manage_messages=True)
    async def list_bad_words(self, ctx):
        """Lister les mots interdits pour ce serveur"""
        guild_id = str(ctx.guild.id)
        if guild_id in self.automod_config:
            bad_words = self.automod_config[guild_id].get("bad_words", [])
            if bad_words:
                await ctx.send(f"Liste des mots interdits pour ce serveur: {', '.join(bad_words)}")
            else:
                await ctx.send("Aucun mot interdit configuré pour ce serveur.")
        else:
            await ctx.send("Aucun mot interdit configuré pour ce serveur.")

    @commands.command(name='setspamconfig')
    @commands.has_permissions(manage_messages=True)
    async def set_spam_config(self, ctx, threshold: int, interval: int):
        """Configurer le seuil de spam et l'intervalle de temps pour ce serveur"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.automod_config:
            self.automod_config[guild_id] = {"bad_words": [], "spam_threshold": threshold, "spam_interval": interval, "mention_threshold": 5, "mention_interval": 10}
        else:
            self.automod_config[guild_id]["spam_threshold"] = threshold
            self.automod_config[guild_id]["spam_interval"] = interval
        
        self.save_config()
        await ctx.send(f"Configuration anti-spam mise à jour : {threshold} messages en {interval} secondes.")

    @commands.command(name='setmentionconfig')
    @commands.has_permissions(manage_messages=True)
    async def set_mention_config(self, ctx, threshold: int, interval: int):
        """Configurer le seuil de spam de mentions et l'intervalle de temps pour ce serveur"""
        guild_id = str(ctx.guild.id)
        if guild_id not in self.automod_config:
            self.automod_config[guild_id] = {"bad_words": [], "spam_threshold": 5, "spam_interval": 10, "mention_threshold": threshold, "mention_interval": interval}
        else:
            self.automod_config[guild_id]["mention_threshold"] = threshold
            self.automod_config[guild_id]["mention_interval"] = interval
        
        self.save_config()
        await ctx.send(f"Configuration anti-mention-spam mise à jour : {threshold} mentions en {interval} secondes.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        guild_id = str(message.guild.id)
        user_id = message.author.id
        now = datetime.utcnow()

        # Anti-spam logic
        if guild_id in self.automod_config:
            spam_config = self.automod_config[guild_id]
            threshold = spam_config.get("spam_threshold", 5)
            interval = spam_config.get("spam_interval", 10)
            
            # Add the current message time to the user's message history
            self.message_history[guild_id][user_id].append(now)

            # Remove messages older than the interval
            while self.message_history[guild_id][user_id] and (now - self.message_history[guild_id][user_id][0]).seconds > interval:
                self.message_history[guild_id][user_id].popleft()

            # Check if the user has exceeded the threshold
            if len(self.message_history[guild_id][user_id]) > threshold:
                await message.channel.send(f"{message.author.mention}, vous envoyez des messages trop rapidement. Vous êtes banni.")
                await message.author.ban(reason="Spam")
                return

            # Anti-mention-spam logic
            mention_threshold = spam_config.get("mention_threshold", 5)
            mention_interval = spam_config.get("mention_interval", 10)
            
            mention_count = sum(1 for mention in message.mentions if mention.id != message.author.id)

            if mention_count > 0:
                # Add the current mention time to the user's mention history
                self.mention_history[guild_id][user_id].extend([now] * mention_count)

                # Remove mentions older than the interval
                while self.mention_history[guild_id][user_id] and (now - self.mention_history[guild_id][user_id][0]).seconds > mention_interval:
                    self.mention_history[guild_id][user_id].popleft()

                # Check if the user has exceeded the mention threshold
                if len(self.mention_history[guild_id][user_id]) > mention_threshold:
                    await message.channel.send(f"{message.author.mention}, vous envoyez trop de mentions. Vous êtes banni.")
                    await message.author.ban(reason="Mention Spam")
                    return

        # Check for bad words
        if guild_id in self.automod_config:
            bad_words = self.automod_config[guild_id].get("bad_words", [])
            for word in bad_words:
                if word in message.content.lower():
                    await message.delete()
                    warning_msg = f"{message.author.mention}, votre message a été supprimé car il contient un mot interdit."
                    await message.channel.send(warning_msg, delete_after=10)
                    return

def setup(bot):
    bot.add_cog(AutoMod(bot))
