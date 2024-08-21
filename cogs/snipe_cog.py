import logging
from collections import defaultdict
from typing import List, Dict, Optional

import discord
from discord.ext import commands


class SnipeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deleted_messages: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        self.edited_messages: Dict[int, Dict[int, List[Dict[str, str]]]] = defaultdict(lambda: defaultdict(list))
    

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message) -> None:
        if message.author.bot or message.author == self.bot.user:
            return
        channel_id = message.channel.id
        self.deleted_messages[channel_id].append({
            'content': message.content,
            'author': message.author.display_name
        })
        if len(self.deleted_messages[channel_id]) > 10:
            self.deleted_messages[channel_id] = self.deleted_messages[channel_id][-10:]

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        if before.author.bot or before.author == self.bot.user:
            return
        channel_id = before.channel.id
        message_id = before.id
        self.edited_messages[channel_id][message_id].append({
            'before': before.content,
            'after': after.content,
            'author': before.author.display_name
        })
        if len(self.edited_messages[channel_id][message_id]) > 10:
            self.edited_messages[channel_id][message_id] = self.edited_messages[channel_id][message_id][-10:]

    @commands.command()
    async def snipe(self, ctx, number: Optional[int] = 1) -> None:
        """Snipes the last `number` deleted and edited messages from the channel."""
        try:
            self.bot.logger.info(f"Snipe command invoked by {ctx.author}")
            await ctx.message.delete()

            channel_id = ctx.channel.id
            sniped_messages = []

            if channel_id in self.deleted_messages and self.deleted_messages[channel_id]:
                sniped_messages += [{'type': 'deleted', 'message': msg} for msg in self.deleted_messages[channel_id][-number:]]

            if channel_id in self.edited_messages:
                for message_id, edits in self.edited_messages[channel_id].items():
                    for edit in edits[-number:]:
                        sniped_messages.append({'type': 'edited', 'message': edit})

            sniped_messages = sniped_messages[-number:]

            if sniped_messages:
                for sniped_message in reversed(sniped_messages):
                    message_type = sniped_message['type']
                    content = sniped_message['message']['content'] if message_type == 'deleted' else sniped_message['message']['after']
                    author = sniped_message['message']['author']
                    before_content = sniped_message['message'].get('before', None)
                    message = (
                        "```ansi\n"
                        "\u001b[2;34m>Last {type} Message:\u001b[0m \u001b[2;33m{content}\u001b[0m\n"
                        "\u001b[2;34m>Author:\u001b[0m \u001b[2;33m{author}\u001b[0m\n"
                    ).format(type='Deleted' if message_type == 'deleted' else 'Edited', content=content, author=author)
                    
                    if message_type == 'edited' and before_content:
                        message += (
                            "\u001b[2;34m>Before:\u001b[0m \u001b[2;33m{before_content}\u001b[0m\n"
                        ).format(before_content=before_content)
                    
                    message += "```"

                    self.bot.logger.info(f"Sniped {message_type} message:\n{message.replace('```ansi\n', '').replace('```', '')}")
                    await ctx.send(message)
            else:
                channel = ctx.channel
                if isinstance(channel, discord.DMChannel):
                    channel_name = "DM Channel"
                elif isinstance(channel, discord.GroupChannel):
                    channel_name = "Group Channel"
                else:
                    channel_name = channel.name
                await ctx.send(f"No messages to snipe in {channel_name}.")
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

async def setup(bot):
    await bot.add_cog(SnipeCog(bot))
