import logging
import traceback

from discord.ext import commands
import discord
import asyncio

logger = logging.getLogger("Nexus-selfbot")

class Clone:

    @staticmethod
    async def delete_roles(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    logger.info(f"Role deleted: {role.name}")
            except discord.Forbidden:
                logger.error(f"Insufficient permissions to delete role: {role.name}")
            except discord.HTTPException:
                logger.error(f"Failed to delete role: {role.name}")
            await asyncio.sleep(0.5)

    @staticmethod
    async def create_roles(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = [role for role in reversed(guild_from.roles) if role.name != "@everyone"]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    mentionable=role.mentionable,
                    hoist=role.hoist
                )
                logger.info(f"Created Role: {role.name}")
            except discord.Forbidden:
                logger.error(f"Insufficient permissions to create role: {role.name}")
            except discord.HTTPException:
                logger.error(f"Failed to create role: {role.name}")

    @staticmethod
    async def delete_channels(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                logger.info(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                logger.error(f"Insufficient permissions to delete channel: {channel.name}")
            except discord.HTTPException:
                logger.error(f"Failed to delete channel: {channel.name}")

    @staticmethod
    async def create_categories(guild_to: discord.Guild, guild_from: discord.Guild):
        for category in guild_from.categories:
            try:
                overwrites = {}
                for key, value in category.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    if role is not None:
                        overwrites[role] = value
                    else:
                        logger.warning(f"Role {key.name} not found in target guild. Skipping overwrite for this role.")
                        
                new_category = await guild_to.create_category(
                    name=category.name, 
                    overwrites=overwrites
                )
                await new_category.edit(position=category.position)
                logger.info(f"Created category: {category.name}")
            except discord.Forbidden:
                logger.error(f"Insufficient permissions to create category: {category.name}")
            except discord.HTTPException:
                logger.error(f"Failed to create category: {category.name}")
            except Exception as e:
                logger.error(f"An unexpected error occurred while creating category: {category.name}, Error: {e}")
                logger.error(traceback.format_exc())

    @staticmethod
    async def create_channels(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            categories_by_name = {category.name: category for category in guild_to.categories}
            logger.debug(f"Categories in target guild: {categories_by_name}")

            for channel_text in guild_from.text_channels:
                try:
                    category = categories_by_name.get(channel_text.category.name) if channel_text.category else None
                    overwrites = {
                        discord.utils.get(guild_to.roles, name=key.name): value
                        for key, value in channel_text.overwrites.items()
                        if discord.utils.get(guild_to.roles, name=key.name) is not None
                    }

                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw
                    )
                    if category:
                        await new_channel.edit(category=category)
                    logger.info(f"Created text channel: {channel_text.name}")
                except Exception as e:
                    logger.error(f"Failed to create text channel: {channel_text.name}, Error: {e}")
                    logger.error(traceback.format_exc())

            for channel_voice in guild_from.voice_channels:
                try:
                    category = categories_by_name.get(channel_voice.category.name) if channel_voice.category else None
                    overwrites = {
                        discord.utils.get(guild_to.roles, name=key.name): value
                        for key, value in channel_voice.overwrites.items()
                        if discord.utils.get(guild_to.roles, name=key.name) is not None
                    }

                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit
                    )
                    if category:
                        await new_channel.edit(category=category)
                    logger.info(f"Created voice channel: {channel_voice.name}")
                except Exception as e:
                    logger.error(f"Failed to create voice channel: {channel_voice.name}, Error: {e}")
                    logger.error(traceback.format_exc())
        except Exception as e:
            logger.error(f"An unexpected error occurred while creating channels, Error: {e}")
            logger.error(traceback.format_exc())



class ServerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def copy_server(self, ctx, server_id_from: int, server_id_to: int):
        try:
            guild_from = self.bot.get_guild(server_id_from)
            guild_to = self.bot.get_guild(server_id_to)

            if guild_from is None or guild_to is None:
                logger.error("One of the specified guilds could not be found.")
                temp = await ctx.send("One of the specified guilds could not be found.")
                await asyncio.sleep(1.5)
                await temp.delete()
                return

            await ctx.send("`Cloning server... This may take a while.`")
            logger.debug("Cloning server... This may take a while.")

            await Clone.delete_roles(guild_to)
            await Clone.delete_channels(guild_to)
            await Clone.create_roles(guild_to, guild_from)
            await Clone.create_categories(guild_to, guild_from)
            try:
                await Clone.create_channels(guild_to, guild_from)
            except Exception as e:
                logger.error(f"Failed to create channels: {e}")
                logger.error(traceback.format_exc())
                temp = await ctx.send("`Failed to clone server.`")
                await asyncio.sleep(1.5)
                await temp.delete()
                return

            await asyncio.sleep(5)
            try:
                await ctx.send("`Server cloned successfully.`")
            except discord.HTTPException:
                pass
            logger.info("Server cloned successfully.")
            temp_message = await ctx.send("`Server cloned successfully.`")
            await asyncio.sleep(3)
            await temp_message.delete()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            logger.error(traceback.format_exc())
            temp_message = await ctx.send("`Failed to clone server.`")
            await asyncio.sleep(3)
            await temp_message.delete()

async def setup(bot):
    await bot.add_cog(ServerCog(bot))
