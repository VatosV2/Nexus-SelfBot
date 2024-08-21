import time
import re

import discord
from discord.ext import commands

class NitroSniperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @staticmethod
    def resolve_gift(code: str) -> str | None:
        rx = r'(?:https?\:\/\/)?(?:discord(?:app)?\.com\/(?:gifts|billing\/promotions)|promos\.discord\.gg|discord.gift)\/(.+)'
        m = re.match(rx, code)
        if m:
            return m.group(1)

    @commands.Cog.listener()
    async def on_message(self, message):
        """Listens for messages and snipes Nitro codes."""
        try:
            if message.author.bot:
                return

            code = self.resolve_gift(message.content)
            if code:
                time_start = time.perf_counter()
                self.bot.logger.info(f"Sniped Nitro Code: {code}")
                
                if len(code) < 16 or len(code) > 24:
                    self.bot.logger.error(f"Invalid Nitro Code Length: {code}")
                    return
                
                try:
                    response = await self.bot.http.redeem_gift(code)

                    time_taken = time.perf_counter() - time_start
                    self.bot.logger.debug(f"Time Taken: {time_taken:.4f} seconds")
                        
                    if response.status_code == 200:
                        await message.add_reaction("🎉")
                        self.bot.logger.info(f"Successfully Redeemed Nitro Code: {code}")
                    elif response.status_code == 400 and 'This gift has been redeemed already' in response.text:
                        self.bot.logger.error(f"Already Redeemed Nitro Code: {code}")
                    elif response.status_code == 404:
                        self.bot.logger.error(f"Invalid Nitro Code: {code}")
                    else:
                        self.bot.logger.error(f"Failed to Redeem Nitro Code: {code} - Status: {response.status_code}, Response: {response.text}")
                except discord.errors.NotFound:
                    self.bot.logger.error(f"Code is invalid or has already been redeemed: {code}")
                except Exception as e:
                    self.bot.logger.error(f"An unexpected error occurred: {e}")
    
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")



async def setup(bot):
    await bot.add_cog(NitroSniperCog(bot))
