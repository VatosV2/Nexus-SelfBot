from discord.ext import commands
import discord

import asyncio
from colorama import Fore

class AdminCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx) -> None:
        """Deletes current channel and creates a new one with the same name and permissions."""
        try:
            await ctx.message.delete()
            channel = await ctx.channel.clone()
            await ctx.channel.delete()
            await channel.send(f"Nuked by `{ctx.author}`")
            self.bot.logger.info(f"Nuked {Fore.GREEN}{channel}{Fore.RESET}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {Fore.RED}{e}{Fore.RESET}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = None) -> None:
        """Kicks the provided member from the server."""
        try:
            await ctx.message.delete()
            await member.kick(reason=reason)
            self.bot.logger.info(f"Kicked {Fore.GREEN}{member}{Fore.RESET} from {Fore.GREEN}{ctx.guild}{Fore.RESET}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {Fore.RED}{e}{Fore.RESET}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = None) -> None:
        """Bans the provided member from the server."""
        try:
            await ctx.message.delete()
            await member.ban(reason=reason)
            self.bot.logger.info(f"Banned {Fore.GREEN}{member}{Fore.RESET} from {Fore.GREEN}{ctx.guild}{Fore.RESET}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {Fore.RED}{e}{Fore.RESET}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx) -> None:
        """Locks the current channel."""
        try:
            await ctx.message.delete()
            for role in ctx.guild.roles:
                if not role.permissions.administrator:
                    await ctx.channel.set_permissions(role, send_messages=False)
            self.bot.logger.info(f"Locked {Fore.GREEN}{ctx.channel}{Fore.RESET}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {Fore.RED}{e}{Fore.RESET}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx) -> None:
        """Unlocks the current channel."""
        try:
            await ctx.message.delete()
            for role in ctx.guild.roles:
                await ctx.channel.set_permissions(role, send_messages=True)
            self.bot.logger.info(f"Unlocked {Fore.GREEN}{ctx.channel}{Fore.RESET}")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {Fore.RED}{e}{Fore.RESET}")

    @nuke.error
    @kick.error
    @ban.error
    @lock.error
    @unlock.error
    async def handle_missing_permissions(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            tmep_message = await ctx.send(f"`Sorry {ctx.author.mention}, you do not have the required permissions to use this command.`")
            await asyncio.sleep(3)
            tmep_message.delete()

async def setup(bot):
    await bot.add_cog(AdminCog(bot))
