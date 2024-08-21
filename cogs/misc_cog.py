from typing import Optional, Set

from discord.ext import commands
import discord

import asyncio

from colorama import Fore
from googletrans import Translator, LANGUAGES

class UtilCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.auto_read_channel: Optional[discord.TextChannel] = None
        self.auto_read_log: bool = True
        self.translator = Translator()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listens for messages and logs them as processed if the auto_read_channel is set."""
        if message.channel == self.auto_read_channel:
            if message.author == self.bot.user:
                return
            try:
                self.bot.ack_message(channel_id=message.channel.id, message_id=message.id)
            except Exception as e:
                self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def auto_read(self, ctx) -> None:
        """Logs all messages in the channel as processed."""
        try:
            await ctx.message.delete()
            self.auto_read_channel = ctx.channel
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(alias="stop_auto_read")
    async def disable_auto_read(self, ctx) -> None:
        """Disables the auto_read_channel."""
        try:
            await ctx.message.delete()
            self.auto_read_channel = None
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def report_message(self, ctx, message_link: Optional[str] = None):
        """Reports the message that the command is replying to or by link."""

        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete command message: {e}")

        message = None
        if ctx.message.reference and not message_link:
            try:
                message = await ctx.fetch_message(ctx.message.reference.message_id)
            except Exception as e:
                self.bot.logger.error(f"Failed to fetch referenced message: {e}")
                return
        elif message_link:
            

            channel_id, message_id = self.get_message_deatils(message_link)
            try:
                channel = self.bot.get_channel(int(channel_id))
                if channel:
                    message = await channel.fetch_message(int(message_id))
                else:
                    self.bot.logger.error(f"Channel not found: {channel_id}")

            except Exception as e:
                self.bot.logger.error(f"Failed to fetch message from link: {e}")
                temp_message = await ctx.send("`Failed to fetch the message from the provided link.`")
                await asyncio.sleep(3)
                await temp_message.delete()
                return
        else:
            self.bot.logger.error("No message link or reply found.")
            temp_message = await ctx.send("`Please reply to a message or provide a valid message link.`")
            await asyncio.sleep(3)
            await temp_message.delete()
            return

        try:
            for _ in range(15):  
                self.bot.mobile_report(guild_id=message.guild.id, channel_id=message.channel.id, message_id=message.id, reason="spam")
                await asyncio.sleep(0.3)

        except Exception as e:
            self.bot.logger.error(f"An error occurred during the report: {e}")
        
        try:
            temp_message = await ctx.send("`Message reported.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to send response message: {e}")

        
    @commands.command()
    async def mass_dm(self, ctx, *, message: str):
        """DMs all friends and open DM channels without sending twice to the same person."""
        try:
            await ctx.message.delete()
            if not ctx.author == self.bot.user:
                await ctx.send("This command can only be used by the owner.")
                return

            sent_users: Set[int] = set()

            for friend in self.bot.relationships:
                if friend.type == discord.RelationshipType.friend:
                    user = friend.user
                    if user.id not in sent_users:
                        try:
                            await user.send(message)
                            sent_users.add(user.id)
                            self.bot.logger.info(f"DM sent to {user.name}")
                        except discord.Forbidden:
                            self.bot.logger.error(f"Could not DM {user.name}")
                        except discord.HTTPException as e:
                            self.bot.logger.error(f"Failed to send message to {user.name}: {e}")

            for channel in self.bot.private_channels:
                    if isinstance(channel, discord.DMChannel):
                        user = channel.recipient
                        if user.id not in sent_users:
                            try:
                                await user.send(message)
                                sent_users.add(user.id)
                                self.bot.logger.info(f"DM sent to {Fore.GREEN}{user.name}{Fore.RESET}")
                            except discord.Forbidden:
                                self.bot.logger.error(f"Could not DM {Fore.RED}{user.name}{Fore.RESET}")
                            except discord.HTTPException as e:
                                self.bot.logger.error(f"Failed to send message to {Fore.RED}{user.name}: {e}{Fore.RESET}")

            temp_message = await ctx.send("`Finished sending DMs.`")
            await asyncio.sleep(3)
            await temp_message.delete()

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def ping(self, ctx):
        """Returns the bot's latency."""
        try:   
            await ctx.message.delete()
            await ctx.send(f"""
```ansi
[2;35m[2;37mPong:[0m[2;35m {round(self.bot.latency * 1000)}ms
[0m
```""")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def translate(self, ctx, *, text: str = None):
        """Translates the provided text to English. You can also reply to a message to translate it."""
        try:
            await ctx.message.delete()

            if ctx.message.reference:
                referenced_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
                text = referenced_message.content
            
            if not text:
                await ctx.send("Please provide some text or reply to a message to translate.")
                return

            translated = self.translator.translate(text, dest='en')
            source_lang = LANGUAGES.get(translated.src, 'unknown').capitalize()
            await ctx.send(f"""
```ansi
[2;35m[Nexus Selfbot - Translator]

[2;37mOriginal Language: [2;35m[2;37m[0m[2;35m[0m[2;37m[2;35m{source_lang}[0m[2;37m[0m[2;35m
[2;37mOriginal Message:[0m[2;35m {text}

[2;37mTranslated Language:[0m[2;35m English[0m
Translated Message: [2;35m{translated.text}[0m

Made by [2;35mvatos.py[0m
```
""")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
            await ctx.send("An error occurred while trying to translate the text.")
    
    @commands.command()
    async def quit(self, ctx):
        """Quits the bot."""
        try:
            await ctx.message.delete()
            self.bot.logger.info("Quitting...")
            temp_message = await ctx.send("`Quitting...`")
            await asyncio.sleep(3)
            await temp_message.delete()
            await self.bot.close()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(UtilCog(bot))