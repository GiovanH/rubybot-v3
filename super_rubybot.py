import discord
from discord.ext import commands
import pickle
import asyncio
import traceback
import logging

import super_rubybot_tumblr as srb_tumblr
import super_rubybot_logger as srb_logger
import super_rubybot_cmds as srb_commands
import super_rubybot_emotes as srb_emotes
import super_rubybot_fluff as srb_fluff
import super_rubybot_servers as srb_servers

from snip import ContextPrinter
print = ContextPrinter(vars(), width=20)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# 499047816807841813
# https://discordapp.com/api/oauth2/authorize?client_id=499047816807841813&scope=bot&permissions=1


class Rubybot(commands.Bot):

    async def on_ready(self):

        # Pre-init
        print('Logged on as {0}!'.format(self.user))
        game = discord.Game("loading...")
        await self.change_presence(status=discord.Status.idle, activity=game)

        # Load managers
        self.emotemgr = srb_emotes.EmoteManager(self)

        # Load modules
        self.tumblrmodule = srb_tumblr.TumblrModule(self, asyncio.get_event_loop(), self.get_channel)
        self.loggermodule = srb_logger.LoggerModule(self)
        self.cmdmodule = srb_commands.CommandModule(self)
        self.fluffmodule = srb_fluff.FluffModule(self)

        # Server-specific code
        self.lwuserver = srb_servers.LWUServer(self)
        self.altgenserver = srb_servers.AltServer(self)

        # Post-init
        game = discord.Game("with myself")
        await self.change_presence(status=discord.Status.idle, activity=game)
        print("Fully ready.")

    async def on_command_error(self, ctx, exc, *args, **kwargs):
        from discord.ext.commands import errors
        if isinstance(exc, errors.MissingRequiredArgument):
            if ctx.message:
                await ctx.message.channel.send("Error: Command is missing a required argument.\n\"{exc}\"\nUse {prefix}help {cmdname} for help.".format(
                    exc=exc, prefix=self.command_prefix, cmdname=ctx.command)
                )
                return
        if isinstance(exc, Exception):
            traceback.format_exception_only(type(exc), exc)
        try:
            raise exc
        except Exception:
            traceback.print_exc()
        await super().on_error(ctx, exc, *args, **kwargs)

    def get_member(self, guild):
        return guild.get_member(self.user.id)

    async def stop(self):
        await self.logout()


def run():
    rubybot = Rubybot(
        command_prefix="$",
        case_insensitive=True
    )

    with open("token", 'rb') as filehandler:
        token = pickle.load(filehandler)

# running = True
# while running:
    try:
        rubybot.run(token)
    except KeyboardInterrupt as e:
        rubybot.stop()


def main():
    run()


if __name__ == "__main__":
    main()
