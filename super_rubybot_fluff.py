from snip.stream import ContextPrinter
print = ContextPrinter(vars(), width=20)

class FluffModule(object):
    def __init__(self, bot):
        super(FluffModule, self).__init__()
        self.bind(bot)
        print("Ready.")

    def bind(self, bot):
        @bot.listen()
        async def on_message(message):
            if message.author == bot.user:
                return
            # tic = time.clock()
            # we do not want the bot to react to itself
            if message.guild is not None:  # Generic Server
                if "rubybot" in message.content.lower():
                    await message.add_reaction(await bot.emotemgr.emote(message.guild, 'smolrubes', False))

                if "boobybot" in message.content.lower():
                    await message.add_reaction(await bot.emotemgr.emote(message.guild, 'rubyblush', False))

                if "wwheek" in message.content.lower():
                    await message.add_reaction('💚')
