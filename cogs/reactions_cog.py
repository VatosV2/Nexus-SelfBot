from typing import Optional, Union
import logging

import discord
from discord.ext import commands

import asyncio


class ReactionsCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.auto_react_user: Optional[Union[discord.User, str]] = None
        self.auto_react_emojis: Optional[str] = None
        self.auto_react_channel: Optional[discord.TextChannel] = None

    async def convert_to_emoji(self, emoji_str: str) -> Union[discord.Emoji, str]:
        """Converts a string to a discord.Emoji object if it's a custom emoji, else returns the string."""

        if emoji_str.startswith("<:") and emoji_str.endswith(">"):
            emoji_id = int(emoji_str.split(":")[-1][:-1])
            emoji = self.bot.get_emoji(emoji_id)
            return emoji or emoji_str
        return emoji_str

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        """Listens for messages and reacts with the auto react emojis if set."""

        if self.auto_react_emojis and self.auto_react_user:
            if (
                self.auto_react_user == "@everyone"
                or message.author == self.auto_react_user
            ):
                if self.auto_react_channel:
                    if message.channel != self.auto_react_channel:
                        return
                    
                for emoji in self.auto_react_emojis.split():
                    try:
                        await message.add_reaction(await self.convert_to_emoji(emoji))
                        self.bot.logger.info(f"Auto reacted with: {emoji}")
                    except discord.HTTPException:
                        self.bot.logger.error(f"Failed to add emoji: {emoji}")
                    except Exception as e:
                        self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def add_reactions(self, ctx, *, type: str) -> None:
        """Adds reactions to a message. Usage: >add_reactions (bomb/emojis)"""
        
        predefined_emojis = [
            "💀", "🔥", "😂",
            "👻", "🌟", "🤣",
            "😊", "🎉", "🐶",
            "🍕", "🌈", "🎶",
            "🍦", "🌺", "🌸",
            "🍔", "🎈", "🐱",
            "🍦", "🌼"
        ]

        if ctx.message.reference is None:
            temp_message = await ctx.send(
                "`Please reply to a message to add reactions.`"
            )
            await asyncio.sleep(3)
            await temp_message.delete()
            return

        reference = ctx.message.reference
        try:
            replied_message = await ctx.channel.fetch_message(reference.message_id)

            if type == "bomb":
                for emoji in predefined_emojis:
                    try:
                        await replied_message.add_reaction(emoji)
                        self.bot.logger.info(f"Bomb reaction added: {emoji}")
                    except discord.HTTPException:
                        self.bot.logger.error(f"Failed to add emoji: {emoji}")
                    except Exception as e:
                        self.bot.logger.error(f"An error occurred: {e}")

                self.bot.logger.info("Bomb reactions added.")
                temp_message = await ctx.send("`Bomb reactions added.`")
                await asyncio.sleep(3)
                await temp_message.delete()
            else:
                emoji_list = type.split()
                for emoji in emoji_list:
                    try:
                        await replied_message.add_reaction(
                            await self.convert_to_emoji(emoji)
                        )
                        self.bot.logger.info(f"Custom reaction added: {emoji}")
                    except discord.HTTPException:
                        self.bot.logger.error(f"Failed to add emoji: {emoji}")
                    except Exception as e:
                        self.bot.logger.error(f"An error occurred: {e}")
                temp_message = await ctx.send("`Custom reactions added.`")
                await asyncio.sleep(3)
                await temp_message.delete()

        except discord.errors.NotFound:
            temp_message = await ctx.send("`Message not found.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            temp_message = await ctx.send(f"An error occurred: `{e}`")
            await asyncio.sleep(3)
            await temp_message.delete()

    @commands.command()
    async def auto_react(self, ctx, user: str, *, emojis: str) -> None:
        """Automatically react to messages with the provided emojis."""

        try:
            await ctx.message.delete()
        except discord.errors.NotFound:
            self.bot.logger.error("Message not found.")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

        if user != "@everyone":
            try:
                self.auto_react_channel = None
                user_obj = await commands.UserConverter().convert(ctx, user)
                self.auto_react_user = user_obj
            except commands.UserNotFound:
                temp_message = await ctx.send(f"User `{user}` not found.")
                await asyncio.sleep(3)
                await temp_message.delete()
                return
        else:
            self.auto_react_user = "@everyone"
            self.auto_react_channel = ctx.channel

        self.auto_react_emojis = emojis
        self.bot.logger.debug(f"Auto reacting with emojis: {emojis} for user: {user}")
        temp_message = await ctx.send(
            f"Auto reacting with emojis: {emojis} for user: {user}"
        )
        await asyncio.sleep(3)
        await temp_message.delete()


    @commands.command()
    async def stop_react(self, ctx) -> None:
        """Disables the auto reacting feature."""

        await ctx.message.delete()
        self.auto_react_emojis = None
        self.auto_react_user = None
        self.auto_react_channel = None
        self.bot.logger.debug("Auto reacting disabled.")
        temp_message = await ctx.send("Auto reacting `disabled`.")
        await asyncio.sleep(3)
        await temp_message.delete()
        
async def setup(bot):
    await bot.add_cog(ReactionsCog(bot))
