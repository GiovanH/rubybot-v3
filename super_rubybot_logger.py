import datetime
import os

from snip.stream import ContextPrinter
print = ContextPrinter(vars(), width=20)

message_format = {
    "on_message_edit": '**{0.author}** edited their message from: "{1.content}" to "{0.content}"',
    "on_message_delete": '{0.author.name} has deleted the message: "{0.content}"',
    "on_message": '',
    "on_member_update": "Nickname change: {before.nick} -> {after.nick}",
    "logmessage": '[{guildname}] #{channelname}\t{authorreal}/{authornick}:\t{message}',
    "timestamp": '[{}] '
}


def format_message(message):
    return message_format['logmessage'].format(
        guildname=message.guild.name if message.guild else "@me direct",
        channelname=message.channel.name if message.guild else message.author.name,
        authorreal="{}#{}".format(message.author.name, message.author.discriminator),
        authornick=message.author.nick if message.guild and message.author.nick else None,
        message=message.clean_content
    )


def logpath(message):
    from slugify import slugify
    if message.guild is not None:
        _dir = os.path.join("logs", slugify(message.channel.guild.name), slugify(message.channel.name))
    else:
        _dir = os.path.join("logs", "direct", slugify(message.author.name))
    os.makedirs(_dir, exist_ok=True)
    return os.path.join(_dir, str(datetime.date.today()) + ".log")


class LoggerModule():
    def __init__(self, bot, stdout=True, file=True):
        super(LoggerModule, self).__init__()
        self.bind(bot)
        self.bot = bot
        self.file = file
        self.stdout = stdout
        print("Ready.")

    def bind(self, bot):
        @bot.listen()
        async def on_message(message):
            if self.stdout:
                print(
                    message_format['timestamp'].format(datetime.datetime.now()),
                    message_format['on_message'].format(message),
                    format_message(message)
                )
            if self.file:
                with open(logpath(message), 'a+', encoding="utf-8") as file:
                    file.write(message_format['timestamp'].format(datetime.datetime.now()))
                    file.write(message_format['on_message'].format(message))
                    file.write("\n")
                    file.write(format_message(message))
                    file.write("\n")

        @bot.listen()
        async def on_message_delete(message):
            if self.stdout:
                print(
                    message_format['timestamp'].format(datetime.datetime.now()),
                    message_format['on_message_delete'].format(message),
                    format_message(message)
                )
            if self.file:
                with open(logpath(message), 'a+', encoding="utf-8") as file:
                    file.write(message_format['timestamp'].format(datetime.datetime.now()))
                    file.write(message_format['on_message_delete'].format(message))
                    file.write("\n")
                    file.write(format_message(message))
                    file.write("\n")

        @bot.listen()
        async def on_message_edit(before, after):
            if before.content == after.content:
                return
            if self.stdout:
                print(
                    message_format['timestamp'].format(datetime.datetime.now()),
                    message_format['on_message_edit'].format(after=after, before=before)
                )
            if self.file:
                with open(logpath(after), 'a+', encoding="utf-8") as file:
                    file.write(message_format['timestamp'].format(datetime.datetime.now()))
                    file.write(message_format['on_message_edit'].format(after=after, before=before))
                    file.write("\n")

        @bot.listen()
        async def on_member_update(before, after):
            if before.nick == after.nick:
                return
            if self.stdout:
                print(
                    message_format['timestamp'].format(datetime.datetime.now()),
                    message_format['on_member_update'].format(before, after)
                )
            if self.file:
                with open(os.path.join("logs", "global"), 'a+', encoding="utf-8") as file:
                    file.write(message_format['timestamp'].format(datetime.datetime.now()))
                    file.write(message_format['on_member_update'].format(before=before, after=after))
                    file.write("\n")
