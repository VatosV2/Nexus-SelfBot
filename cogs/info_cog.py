from typing import List

from discord.ext import commands
import discord

import asyncio

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def user_info(self, ctx, user: discord.User) -> None:
        """Displays information about the mentioned user."""
        self.bot.logger.info(f"User info requested by {ctx.author.name} for {user.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        try:
            
            text = f"""
```ansi
[2;35m[User Info - {user.name}][0m

[2;37mGlobalName:[0m[2;35m {user.name}
[2;37mID:[0m[2;35m {user.id}
[2;37mCreated At:[0m[2;35m {user.created_at}
[2;37mAvatar:[0m[2;35m {user.avatar.url if user.avatar else "No Avatar"}
[2;37mBannner:[0m[2;35m {user.banner.url if user.banner else "No Banner"}

[2;37mMade By[0m[2;35m vatos.py[0m
```
"""
            if user.avatar:
                text += f"[Avatar URL]({user.avatar.url})\n"
            if user.banner:
                text += f"[Banner URL]({user.banner.url})\n"

            await ctx.send(text)
        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending user info: {e}")
    
    @commands.command()
    async def server_info(self, ctx) -> None:
        """Displays information about the server."""
        self.bot.logger.info(f"Server info requested by {ctx.author.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        if ctx.guild is None:
            temp = await ctx.send("`This command can only be used in a server.`")
            await asyncio.sleep(1.5)
            await temp.delete()
            self.bot.logger.error("This command can only be used in a server.")
            return

        try:
            guild = ctx.guild
            text = f"""
```ansi
[2;35m[Server Info - {guild.name}][0m

[2;35m[2;37mServerName:[0m[2;35m {guild.name}
[2;37mID:[0m[2;35m {guild.id}
[2;37mCreated At:[0m[2;35m {guild.created_at}
[2;37mOwner:[0m[2;35m {guild.owner}
[2;37mMembers:[0m[2;35m {guild.member_count}
[2;37mRoles:[0m[2;35m {len(guild.roles)}
[2;37mChannels:[0m[2;35m {len(guild.channels)}
[2;37mCategories:[0m[2;35m {len(guild.categories)}
[2;37mServerIcon:[0m[2;35m {guild.icon.url if guild.icon else "No Icon"}
[2;37mServerBanner:[0m[2;35m {guild.banner.url if guild.banner else "No Banner"}

[2;37mMade By[0m[2;35m vatos.py[0m
```
"""
            if guild.icon:
                text += f"[Server Icon URL]({guild.icon.url})\n"
            if guild.banner:
                text += f"[Server Banner URL]({guild.banner.url})\n"

            await ctx.send(text)

        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending server info: {e}")
    
    @commands.command()
    async def gc_info(self, ctx) -> None:
        """Displays information about the global context."""
        self.bot.logger.info(f"Group Chat info requested by {ctx.author.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        if not isinstance(ctx.channel, discord.GroupChannel):
            self.bot.logger.error("This command can only be used in a group chat.")
            temp = await ctx.send("`This command can only be used in a group chat.`")
            await asyncio.sleep(1.5)
            await temp.delete()
            return

        group_chat: discord.GroupChannel = ctx.channel
        try:
            text = f"""
```ansi
[2;35m[Group Chat Info - {group_chat.name}][0m

[2;37mGroupName:[0m [2;35m{group_chat.name}[0m
[2;37mID:[0m [2;35m{group_chat.id}[0m
[2;37mCreated At:[0m [2;35m[2;35m{group_chat.created_at}[0m[2;35m[0m
[2;37mOwner:[0m [2;35m{group_chat.owner}[0m
[2;37mMembers:[0m [2;35m{len(group_chat.recipients) + 1}[0m
[2;37mIcon:[0m [2;35m[2;35m{group_chat.icon.url if group_chat.icon else "No Icon"}[0m[2;35m[0m

[2;37mMade By[0m [2;35mvatos.py[0m
```
"""
            if group_chat.icon:
                text += f"[Icon URL]({group_chat.icon.url})\n"
            await ctx.send(text)

        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending group chat info: {e}")

    
    @commands.command()
    async def my_info(self, ctx) -> None:
        """Displays information about the author."""
        self.bot.logger.info(f"User info requested by {ctx.author.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        try:
            user = ctx.author
            text = f"""
```ansi
[2;35m[User Info - {user.name}][0m

[2;37m[0m[2;37mSever Count:[0m [2;35m{len(self.bot.guilds)}[0m
[2;37mOwned Servers:[0m [2;35m{len([guild for guild in self.bot.guilds if guild.owner == user])}[0m
[2;37mFriend Count:[0m [2;35m{len(self.bot.friends)}[0m
[2;37mOpen DMs:[0m [2;35m{len(self.bot.private_channels)}
[2;37mBlocked Users:[0m [2;35m{len(self.bot.blocked)}[0m
[0m[2;37mGroups:[0m[2;35m {len([channel for channel in self.bot.private_channels if isinstance(channel, discord.GroupChannel)])}[0m

[2;37mMade By[0m [2;35mvatos.py[0m
```
"""
            await ctx.send(text)
        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending user info: {e}")

    @commands.command()
    async def services(self, ctx) -> None:
        """Displays information about the services."""
        self.bot.logger.info(f"Services info requested by {ctx.author.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        try:
            response_cog = self.bot.get_cog("ResponseCog")
            reactions_cog = self.bot.get_cog("ReactionsCog")
            util_cog = self.bot.get_cog("UtilCog")
            

            text = f"""
```ansi
[2;35m[Running Services]
[0m
[2;35mNitro Sniper [2;37m/ [2;36mON[0m[2;37m[0m[2;35m
[2;35mMessage Sniper [2;37m/ [2;36mON[0m[2;37m[0m[2;35m
[2;35mAuto Responder [2;37m/ {"[2;31m[2;36mON[0m[2;31m[0m" if response_cog and response_cog.auto_response_message is not None else "[2;31mOFF[0m"}
[2;35mAuto Reactor [2;37m/ {"[2;31m[2;36mON[0m[2;31m[0m" if reactions_cog and reactions_cog.auto_react_user is not None else "[2;31mOFF[0m"}
[2;35mAuto Reader [2;37m/ {"[2;31m[2;36mON[0m[2;31m[0m" if util_cog and util_cog.auto_read_channel is not None else "[2;31mOFF[0m"}
[2;35mUser Responder [2;37m/ {"[2;31m[2;36mON[0m[2;31m[0m" if response_cog and response_cog.response_user_message is not None else "[2;31mOFF[0m"}
[2;35mCopy Cat [2;37m/ {"[2;31m[2;36mON[0m[2;31m[0m" if util_cog and response_cog.copy_cat_user is not None else "[2;31mOFF[0m"}

[2;37mMade by[0m[2;36m [2;35mvatos.py[0m[2;36m[0m[2;37m[0m[2;35m[0m
```
"""
            await ctx.send(text)
        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending services info: {e}")

    @commands.command(name="bot_info")
    async def selfbot_info(self, ctx) -> None:
        """Displays information about the bot."""
        self.bot.logger.info(f"Bot info requested by {ctx.author.name}")
        try:
            await ctx.message.delete()
        except Exception as e:
            self.bot.logger.error(f"Failed to delete message: {e}")

        try:
            text = f"""
```ansi
[2;35m[Nexus Selfbot - Bot Info]

[2;37m[2;35m[0m[2;37m[0m[2;35m[0m[2;37mDownload Link ~ [2;35mhttps://github.com/VatosV2/Nexus-SelfBot[0m[2;37m
Owner/Developer ~ [2;35mvatosv2/vatos.py[0m[2;37m
Version ~ [2;35m1.0.0

[2;37mmade by[0m[2;35m vatos.py[0m[2;37m[0m
```"""
            await ctx.send(text)
        except Exception as e:
            self.bot.logger.error(f"An error occurred when sending bot info: {e}")
            

async def setup(bot):
    await bot.add_cog(InfoCog(bot))
