from typing import List

from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.HELPLIST: List[str] = [
"""
```ansi
[2;35m[Nexus Selfbot - Help Commands]
[0m[2;35m
>help.packing [2;37m/ Shows Packing Commands
[2;35m>help.auto_response [2;37m/ Shows Auto Response Commands
[2;35m>help.misc [2;37m/ Shows Misc Commands
[2;35m>help.gc [2;37m/ Shows GC Commands
[2;35m>help.reactions [2;37m/Shows Reaction Commands
[2;36m[2;35m>help.spam[0m[2;36m[0m[2;37m / Shows Spam Commands
[2;35m>help.admin [2;37m/ Shows Admin Commands
[2;35m>help.info[0m[2;37m / Shows Info Commands

[2;35m>help.all [2;37m/ Shows All Commands
[2;35m>services [2;37m/ Shows Running Services
[2;35m>bot_info [2;37m/ Shows Bot Info

[2;35m>quit [2;37m/ Quits The Bot

[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```""",
"""
```ansi
[2;35m[Nexus Selfbot - Pack Commands]
[0m[2;35m
>pack[0m [2;37m/ Starts Packing[0m
[2;35m>stop_pack[0m [2;37m/ Stops Packing[0m
[2;35m>delete_pack[0m [2;37m/ Deletes Last Pack[0m
[2;35m>set_user_response.large [0m[2;37m(user) (message) / Sets auto response for large messages[0m

[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - Auto response][0m

[2;35m>set_delay [0m[2;37m(delay) / Sets delay between messages[0m[2;37m[0m
[2;35m>set_response[0m [2;34m[2;37m(message)[0m[2;34m[0m [2;37m/ Sets auto response on pings[0m
[2;35m>disable_response[0m [2;37m/ Disables auto response
[2;35m>copy_cat [0m[2;37m(user) / Copies everything the user says[0m[2;37m[0m
[2;35m>stop_copy_cat [0m[2;37m/ Stops Copy Catting[0m
[2;35m>set_user_response [0m[2;37m(user) (message) / Sets auto response for a user[0m
[2;35m>set_user_response.large [0m[2;37m(user) (message) / Sets auto response for large messages[0m
[2;35m>stop_user_response [0m[2;37m/ Stops User Response[0m

[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - GC Commands]
[0m[2;35m
>lock_gc [2;37m/ Locks Current GC[0m[2;35m
>unlock_gc [2;37m/ Unlocks Locked GC[0m[2;35m
>auto_name [2;37m/ Spam Changes GC name[0m[2;35m
>stop_auto_name [2;37m/ Stops auto name spam[0m[2;35m
>leave_all_gcs [2;37m (Optional[exceptions by ids]) / Leaves all group channels[0m[2;35m
>mass_add [2;37m(user/s) / Adds and removes user from a GC.[0m[2;35m
>stop_mass_add [2;37m/ Stops Mass Adding[0m[2;35m
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
``` 
""",
"""
```ansi
[2;35m[Nexus Selfbot - Reaction Commands]
[0m[2;35m
>auto_react [2;37m(user) (emojis) / Auto Reacts to messages[0m[2;35m
>stop_react [2;37m/ Stops auto reacting[0m[2;35m
>add_reactions [2;37m(bomb/emojis) / Adds Reactions
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - Spam Commands]
[0m[2;35m
>spam (message)[2;37m / Starts Spamming the defined message.[0m[2;35m
>stop_spam [2;37m/ Stops Spamming[0m[2;35m
>delete_spam [2;37m/ Deletes Last Spam

[0m[2;35m>ghost_ping [2;37m(user) [2;37m/ Spam Ghost Pings user[0m[2;35m
>stop_ghost_ping [2;37m/ Stops Ghost Pinging[0m[2;35m
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - Info Commands]
[0m[2;35m
>user_info [2;37m(user) / Shows User Info[0m[2;35m
>server_info [2;37m/ Shows Server Info[0m[2;35m
>gc_info  [2;37m/ Shows Group chats Info[0m[2;35m
>my_info  [2;37m/ Shows Your Info[0m[2;35m
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m[2;37m[0m[2;35m[0m
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - Admin Commands]
[0m[2;35m
>nuke [2;37m/ Nukes A channel.[0m[2;35m
[0m[2;35m>lock [2;37m/ Locks Current Channel[0m[2;35m[0m
[2;35m>kick [2;37m(user) (Optional[reason]) / Kicks A USer[0m[2;35m[0m
[2;35m>ban [0m[2;37m(user) (Optional[reason]) / Bans A User[0m
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py
```
""",
"""
```ansi
[2;35m[Nexus Selfbot - Misc Commands]
[0m[2;35m
>snipe [2;37m(number) / Snipes last deleted message[0m[2;35m
>copy_server [2;37m(ServerID_from) (serverID_to) / Copys A Server[0m[2;35m
>report_message [2;37m(ReplyToMessage/MessageLink) / Mass Reports a Messages[0m[2;35m
>auto_read [2;37m/ Auto Reads Messages[0m[2;35m
>disable_auto_read [2;37m/ Stops Auto Reading[0m[2;35m
>mass_dm [2;37m(message) / Mass Dms all friends and open dms[0m[2;35m
>ping [2;37m/ Shows Bot Latency[0m[2;35m
>translate [2;37m(text) / Translates Text to English[0m[2;35m
>quit [2;37m/ Quits The Bot[0m[2;35m
[0m
[2;35m[2;37mMade by [0m[2;35mvatos.py
```
"""
        ]


    @commands.command()
    async def help(self, ctx):
        """Displays the help message."""
        try:
            self.bot.logger.info("Help requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[0])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
    
    @commands.command(name="help.packing")
    async def help_packing(self, ctx):
        """Displays the help message for packing commands."""
        try:
            self.bot.logger.info("Help packing requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[1])
        
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
    
    @commands.command(name="help.auto_response")
    async def help_auto_response(self, ctx):
        """Displays the help message for auto response commands."""
        try:
            self.bot.logger.info("Help auto response requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[2])
        
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(name="help.gc")
    async def help_gc(self, ctx):
        """Displays the help message for gc commands."""
        try:
            self.bot.logger.info("Help gc requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[3])
        
        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(name="help.reactions")
    async def help_reactions(self, ctx):
        """Displays the help message for reactions commands."""
        try:
            self.bot.logger.info("Help reactions requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[4])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    @commands.command(name="help.spam")
    async def help_spam(self, ctx):
        """Displays the help message for spam commands."""
        try:
            self.bot.logger.info("Help spam requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[5])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")

    
    @commands.command(name="help.info")
    async def help_info(self, ctx):
        """Displays the help message for info commands."""
        try:
            self.bot.logger.info("Help info requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[6])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")    

    @commands.command(name="help.admin")
    async def help_admin(self, ctx):
        """Displays the help message for admin commands."""
        try:
            self.bot.logger.info("Help admin requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[7])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
    
    @commands.command(name="help.misc")
    async def help_misc(self, ctx):
        """Displays the help message for misc commands."""
        try:
            self.bot.logger.info("Help misc requested.")
            await ctx.message.delete()
            await ctx.send(self.HELPLIST[8])

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")
    
    @commands.command(name="help.all")
    async def help_all(self, ctx):
        """Displays the help message for all commands."""
        try:
            self.bot.logger.info("Help all requested.")
            await ctx.message.delete()
            message = ""
            for help_message in self.HELPLIST[:5]:
                message += help_message  
            await ctx.send(message) 

            message = ""
            for help_message in self.HELPLIST[5:]:
                message += help_message  
            await ctx.send(message) 

        except Exception as e:
            self.bot.logger.error(f"An error occurred: {e}")


    

async def setup(bot):
    await bot.add_cog(HelpCog(bot))