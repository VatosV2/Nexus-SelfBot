from typing import Dict, Set, Optional

from discord.ext import commands
import discord

import asyncio

class GcCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_flag: bool = False
        self.locked_groups: Dict[int, Set[discord.User]] = {}
        self.mass_add_flag: bool = False

    @commands.command()
    async def auto_name(self, ctx, *, name: str) -> None:
        """Automatically change the group channel name."""
        
        await ctx.message.delete()
        count: int = 0
        channel: discord.abc.GuildChannel = ctx.channel

        while not self.spam_flag:
            try:
                await channel.edit(name=f"{name} | {count}")
                self.bot.logger.info(f"Changed channel name to: {name} | {count}")
                count += 1
            except discord.Forbidden:
                self.bot.logger.error("Permission denied to change channel name.")
                break
            except Exception as e:
                self.bot.logger.error(f"An error occurred: {e}")
                break

    @commands.command()
    async def stop_auto_name(self, ctx) -> None:
        """Stop changing the group channel name."""
        try:
            await ctx.message.delete()
            self.spam_flag = True

            self.bot.logger.debug("Stopped changing GC name.")

            temp_message = await ctx.send("`Stopped changing GC name.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def lock_gc(self, ctx) -> None:
        """Lock the group channel by removing non-existing members and preventing new ones."""
        try:
            await ctx.message.delete()

            if isinstance(ctx.channel, discord.GroupChannel):
                group = ctx.channel

                if group.owner == ctx.author:
                    self.locked_groups[group.id] = set(group.recipients)
                    self.bot.logger.info(f"Locked group channel: {group.name}")
                    temp_message = await ctx.send("`The group channel is now locked. No new members can be added.`")
                    await asyncio.sleep(3)
                    await temp_message.delete()
                else:
                    self.bot.logger.error(f"Permission denied to lock group channel: {group.name}")
                    temp_message = await ctx.send("`You do not have permission to lock this group channel.`")
                    await asyncio.sleep(3)
                    await temp_message.delete()
            else:
                self.bot.logger.debug("This command can only be used in a group channel.")
                temp_message = await ctx.send("`This command can only be used in a group channel.`")
                await asyncio.sleep(3)
                await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.Cog.listener()
    async def on_group_join(self, group: discord.GroupChannel, user: discord.User) -> None:
        """Kick any new member who joins if the group is locked."""
        if group.id in self.locked_groups:
            if user not in self.locked_groups[group.id]:
                try:
                    await group.remove_recipients(user)
                    self.bot.logger.info(f"Removed user: {user.display_name}")
                    await group.send(f"""```ansi
[2;31m{user.display_name}[0m tried to join but was removed because the group is locked.
```""")
                except discord.Forbidden:
                    self.bot.logger.error(f"Permission denied to remove user: {user.display_name}")
                except Exception as e:
                    self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def unlock_gc(self, ctx) -> None:
        """Unlock the group channel to allow new members."""
        try:
            await ctx.message.delete()

            if isinstance(ctx.channel, discord.GroupChannel):
                group = ctx.channel
                if group.id in self.locked_groups:
                    del self.locked_groups[group.id]
                    self.bot.logger.info(f"Unlocked group channel: {group.name}")
                    await ctx.send("`The group channel is now unlocked. New members can be added.`")
                else:
                    self.bot.logger.error("The group channel is not locked.")
                    await ctx.send("`The group channel is not locked.`")
            else:
                self.bot.logger.debug("This command can only be used in a group channel.")
                await ctx.send("`This command can only be used in a group channel.`")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command()
    async def leave_all_gcs(self, ctx, exceptions: Optional[discord.GroupChannel] = None) -> None:
        """Leave all group DMs."""
        await ctx.message.delete()

        for dm_channel in self.bot.private_channels:
            if isinstance(dm_channel, discord.GroupChannel):
                try:
                    if dm_channel.id in exceptions:
                        return
                    
                    await dm_channel.leave()
                    self.bot.logger.info(f"Left group DM: {dm_channel.name}")
                except Exception as e:
                    self.bot.logger.error(f"An error occurred: {e}")
        
        self.bot.logger.info("Left all group DMs.")

    @commands.command()
    async def mass_add(self, ctx, *users: discord.User) -> None:
        """Add multiple users to a group channel."""
        try:
            await ctx.message.delete()

            if isinstance(ctx.channel, discord.GroupChannel):
                group = ctx.channel
                self.mass_add_flag = True
                while self.mass_add_flag:
                    for user in users:
                        try:
                            await group.add_recipients(user)
                            self.bot.logger.info(f"Added user: {user.display_name}")
                        except discord.Forbidden:
                            self.bot.logger.error(f"Permission denied to add user: {user.display_name}")
                        except Exception as e:
                            self.bot.logger.error(f"An error occurred: {e}")
                        try:
                            await group.remove_recipients(user)
                            self.bot.logger.info(f"Removed user: {user.display_name}")
                        except discord.Forbidden:
                            self.bot.logger.error(f"Permission denied to remove user: {user.display_name}")
                        except Exception as e:
                            self.bot.logger.error(f"An error occurred: {e}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
    
    @commands.command()
    async def stop_mass_add(self, ctx) -> None:
        """Stop the mass add process"""
        try:
            await ctx.message.delete()
            self.mass_add_flag = False

            self.bot.logger.debug("Stopped mass adding.")

            temp_message = await ctx.send("`Stopped mass adding.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(GcCog(bot))
