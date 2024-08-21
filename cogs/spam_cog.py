import logging
from typing import List, Optional

from discord.ext import commands
import discord

import asyncio

class SpamCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam: bool = False
        self.ghost_ping: bool = False
        self.spam_messages: List[discord.Message] = []

    @commands.command()
    async def spam(self, ctx, *, _message: str) -> None:
        """Spams the provided message in current channel."""
        amount: int = 0

        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

        self.spam = True
        while self.spam:
            try:
                self.bot.logger.info(f"Spammed message: {_message}")
                message = await ctx.send(_message)
                self.spam_messages.append(message)
                amount += 1
            except Exception as e:
                self.bot.logger.error(f"An error occurred: {e}")
        self.bot.logger.info(f"Spammed {amount} messages with: {message}")
    
    @commands.command()
    async def stop_spam(self, ctx) -> None:
        """Stops the spamming process."""
        try:
            await ctx.message.delete()
            self.spam = False

            self.bot.logger.debug("Stopped spamming.")
            temp_message = await ctx.send("`Stopped spamming.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def delete_spam(self, ctx):
        try:
            await ctx.message.delete()
            for message in self.spam_messages:
                await message.delete()
            self.spam_messages = []
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def ghost_ping(self, ctx, user: discord.User) -> None:
        """Ghost pings the provided user."""
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

        self.ghost_ping = True
        while self.ghost_ping:
            try:
                message = await ctx.send(user.mention); await message.delete()
                self.bot.logger.info(f"Ghost pinged user: {user}")
            except Exception as e:
                self.bot.logger.error(f"An error occurred: {e}")
        self.bot.logger.info(f"Ghost pinged user: {user}")
    
    @commands.command()
    async def stop_ghost_ping(self, ctx) -> None:
        """Stops the ghost pinging process."""
        try:
            await ctx.message.delete()
            self.ghost_ping = False

            self.bot.logger.debug("Stopped ghost pinging.")
            temp_message = await ctx.send("`Stopped ghost pinging.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")



async def setup(bot):
    await bot.add_cog(SpamCog(bot))