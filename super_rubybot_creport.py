import os
import traceback
from discord.ext import commands

from snip import ContextPrinter
print = ContextPrinter(vars(), width=20)


class Creport():
    def __init__(self, bot):
        super(Creport, self).__init__()
        self.bot = bot
        self.bind()

    def bind(self):
        bot = self.bot

        @bot.listen()
        async def on_ready():
            gio = bot.get_user(233017800854077441)
            # Load shutdown report
            if os.path.exists("last_trace.log"):
                with open("last_trace.log", "r") as tracefile:
                    await gio.send("I just came online. Last error: \n" + tracefile.read())
            else:
                await gio.send("I just came online. No traceback file exists.")
            with open("git.log", "r") as _file:
                await gio.send("Latest git revision: \n" + _file.read())
            os.unlink("last_trace.log")

        @bot.listen()
        async def on_error(event_method, *args, **kwargs):
            print("caught error")
            print(__name__)
            print(vars())
            with open("last_trace.log", "w") as tracefile:
                tracefile.write(traceback.format_exc())
            await super(commands.Bot, bot).on_error(event_method, *args, **kwargs)

        @bot.listen()
        async def on_command_error(ctx, exc, *args, **kwargs):
            import sys
            print("caught command error")

            from discord.ext.commands import errors
            if isinstance(exc, errors.MissingRequiredArgument):
                if ctx.message:
                    await ctx.message.channel.send("Error: {exc}\nCommand is missing a required argument.\nUse {prefix}help {cmdname} for help.".format(
                        exc=exc, prefix=ctx.bot.command_prefix, cmdname=ctx.command)
                    )
                    return
            elif isinstance(exc, errors.CommandNotFound):
                if ctx.message:
                    if set(ctx.message.content) == set(ctx.bot.command_prefix):
                        # probably just shouting?
                        return 
                    await ctx.message.channel.send("Error: {exc}\nUse {prefix}help for help.".format(
                        exc=exc, prefix=ctx.bot.command_prefix)
                    )
                    return
            print('Exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(exc), exc, exc.__traceback__, file=sys.stderr)
            
            # raise exc
