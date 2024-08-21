import logging
from typing import Optional
import re

from discord.ext import commands
import discord

import asyncio
import httpx
from colorama import Fore

class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_response_message: Optional[str] = None
        self.copy_cat_user: Optional[discord.Member] = None
        self.response_user: Optional[discord.Member] = None
        self.response_user_message: Optional[str] = None
    
    @staticmethod
    def get_message_details(message_link: str) -> tuple:
        match = re.search(r"(?:canary\.|ptb\.)?discord.com/channels/(\d+)/(\d+)/(\d+)", message_link)
        return int(match.group(2)), int(match.group(3))
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listens for messages and responds to pings with the auto response message, unless @everyone is mentioned."""
        if self.bot.user.mentioned_in(message) and not message.mention_everyone:
            if self.auto_response_message:
                await message.channel.send(self.auto_response_message)
                self.bot.logger.info(f"Auto response sent: {self.auto_response_message}")   

        elif self.copy_cat_user:
            if message.author == self.copy_cat_user:
                await message.channel.send(message.content)
                self.bot.logger.info(f"Copy cat message sent: {message.content}")
                
        elif message.author == self.response_user:
            await message.channel.send(self.response_user_message)
            self.bot.logger.info(f"User response sent: {self.response_user_message}")

    @commands.command()
    async def set_response(self, ctx, *, message_content: str) -> None:
        """Sets the auto response message to the provided message."""
        try:
            await ctx.message.delete()
            self.auto_response_message = message_content

            self.bot.logger.debug(f"Auto response message set to: {message_content}")
            temp_message = await ctx.send(f"Auto response message set to `{message_content}`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def set_user_response(self, ctx, user: discord.Member, *, message_content: str) -> None:
        """Sets the auto response message to the provided message."""
        try:
            await ctx.message.delete()
            self.response_user_message = message_content
            self.response_user = user

            self.bot.logger.debug(f"Auto response message set to: {message_content}")
            temp_message = await ctx.send(f"Auto response message set to `{message_content}`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(name="set_user_response.large")
    async def auto_response_large(self, ctx, user: discord.Member, *, message_content: str) -> None:
        """Sets the auto response message to the provided user with large spaces before."""
        try:
            await ctx.message.delete()
            self.response_user_message = "Nexus.." + "\n" * 200 + message_content + user.mention
            self.response_user = user

            self.bot.logger.debug(f"Auto response message set to: {message_content}")
            temp_message = await ctx.send(f"Auto response message set to `{message_content}`")
            await asyncio.sleep(3)
            await temp_message.delete()

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(name="stop_user_response")
    async def disable_user_response(self, ctx) -> None:
        """Disables the auto response message."""
        try:
            await ctx.message.delete()
            self.response_user = None
            self.response_user_message = None

            self.bot.logger.debug("Auto response message disabled")
            temp_message = await ctx.send("Auto response message `disabled`.")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def disable_response(self, ctx) -> None:
        """Disables the auto response message."""
        try:
            await ctx.message.delete()
            self.auto_response_message = None

            self.bot.logger.debug("Auto response message disabled")
            temp_message = await ctx.send("Auto response message `disabled`.")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def copy_cat(self, ctx, user: discord.Member) -> None:
        """Repeat the last message sent by the provided user."""
        try:
            await ctx.message.delete()
            self.copy_cat_user = user
            self.bot.logger.debug(f"Copy catting user: {user}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def stop_copy_cat(self, ctx) -> None:
        """Stop the copy catting process."""
        try:
            await ctx.message.delete()
            self.copy_cat_user = None
            self.bot.logger.debug("Copy catting stopped.")

            temp_message = await ctx.send("`Copy catting stopped.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(ResponseCog(bot))
