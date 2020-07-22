import discord
from discord.ext import commands
import pickle

import super_rubybot_logger as srb_logger
import super_rubybot_creport as srb_creport

from snip.filesystem import easySlug
from datetime import datetime

from snip.singleton import SingleInstance

from snip.stream import std_redirected
import logging

import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

now = datetime.strftime(datetime.now(), "%Y-%m-%d %X")
os.makedirs("./logs/logbot/", exist_ok=True)
logpath = "./logs/logbot/debug {}.log".format(easySlug(now))
logger.info(f"Logpath: {logpath}")
loghandler_file = logging.FileHandler(logpath)

loghandler_file.setLevel(logging.DEBUG)
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loghandler_file.setFormatter(f_format)
logger.addHandler(loghandler_file)


class Logbot(commands.Bot):

    async def on_ready(self):

        # Pre-init
        self.creport = srb_creport.Creport(self)

        logger.info('Logged on as {0}!'.format(self.user))

        self.loggermodule = srb_logger.LoggerModule(self, stdout=False)

    def get_member(self, guild):
        return guild.get_member(self.user.id)

    async def stop(self):
        await self.logout()


def run():
    logbot = Logbot(
        command_prefix="§§LOGBOT",
        case_insensitive=False
    )

    with open("token_logbot", 'rb') as filehandler:
        token = pickle.load(filehandler)

# running = True
# while running:
    with std_redirected(logpath, tee=True):
        try:
            SingleInstance()
            logger.info("Logging in...")
            logbot.run(token, bot=False)
            logger.info("Logged in")
        except KeyboardInterrupt:
            logbot.stop()


def main():
    run()


if __name__ == "__main__":
    main()
