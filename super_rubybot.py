import discord
from discord.ext import commands
import pickle

import super_rubybot_tumblr as srb_tumblr
import super_rubybot_logger as srb_logger
import super_rubybot_cmds as srb_commands
import super_rubybot_emotes as srb_emotes
import super_rubybot_fluff as srb_fluff
import super_rubybot_servers as srb_servers
import super_rubybot_creport as srb_creport

import asyncio

from snip.singleton import SingleInstance

from snip.stream import TriadLogger

logger = TriadLogger(__name__)

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


# print = logger.info

# 499047816807841813
# https://discordapp.com/api/oauth2/authorize?client_id=499047816807841813&scope=bot&permissions=1

class Rubybot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super(Rubybot, self).__init__(*args, **kwargs)
        self.initialized = False

    async def on_ready(self):

        if not self.initialized:
            # Pre-init
            self.creport = srb_creport.Creport(self)
            logger.info('Logged on as {0}!'.format(self.user))
            self.loop = asyncio.get_event_loop()

            # Load managers
            self.emotemgr = srb_emotes.EmoteManager(self)

            # Load modules
            self.tumblrmodule = srb_tumblr.TumblrModule(self, self.get_channel)
            self.loggermodule = srb_logger.LoggerModule(self, stdout=False)
            self.cmdmodule = srb_commands.CommandModule(self)
            self.fluffmodule = srb_fluff.FluffModule(self)

            # Server-specific code
            self.lwuserver = srb_servers.LWUServer(self)
            self.altgenserver = srb_servers.AltServer(self)

            # Post-init
            game = discord.Game("with ur heart <3")
            await self.change_presence(status=discord.Status.idle, activity=game)
            logger.info("Fully ready.")
            self.initialized = True

    # async def on_error(self, event_method, *args, **kwargs):
    #     self.creport.on_error(event_method, *args, **kwargs)

    # async def on_command_error(self, ctx, exc, *args, **kwargs):
    #     self.creport.on_command_error(ctx, exc, *args, **kwargs)
    async def spoolSend(self, messagable, content):
        short = ""
        for line in content.split('\n'):
            short += line + "\n"
            if len(short) >= 1600:
                await messagable.send(content=short)
                short = ""
        await messagable.send(content=short)

    def get_member(self, guild):
        return guild.get_member(self.user.id)

    async def stop(self):
        await self.logout()


def run():

    intents = discord.Intents.default()
    intents.message_content = True

    rubybot = Rubybot(
        command_prefix="!",
        intents=intents,
        case_insensitive=True
    )

    with open("token", 'rb') as filehandler:
        token = pickle.load(filehandler)

    try:
        rubybot.run(token)
    except discord.errors.LoginFailure:
        print("Bad token!")
    except KeyboardInterrupt:
        rubybot.stop()


if __name__ == "__main__":
    SingleInstance()
    while True:
        try:
            run()
            logger.error("Crashed out of main!")
            continue
        except KeyboardInterrupt:
            break
