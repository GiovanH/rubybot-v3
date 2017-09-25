import discord
from discord.ext import commands

gio_id = '233017800854077441'

permissions = {}
servers = {}
commands = {}
direct_commands = {}


def permissionLevel(user, server):
    if user.id == gio_id:
        return 3
    if server == None:
        return 0
    plvl = 0
    for r in user.roles:
        rlvl = permissions.get(server.id).get(r.id)
        if rlvl == None:
            continue
        if plvl < rlvl:
            plvl = rlvl
    return plvl


class Command:
    """A rubybot message commands
    Arguments:
    Name : String representing a human-readable command name
    CB   : Callback function. Must take one argument, a discord.message
    helpstr : A human-readable help document documenting the command
    permlevel : A permission level. 0 = everyone, 1 = mod, 2 = admin, 3 = gio"""

    def __init__(self, name, cb, helpstr, permlevel):
        self.name = name
        self.function = cb
        self.helpstr = helpstr
        self.permlevel = permlevel
        commands.update({name: self})

    async def run(self, message):
        """Attempt to execute command on behalf of message author
        Arg: Message: a discord.Message"""
        if message.content.startswith('!' + self.name):
            if permissionLevel(message.author, message.server) >= self.permlevel:
                await self.function(message)
            else:
                raise NameError('User ' + message.author.name +
                            ' has insufficient permissions to perform command ' + self.name)


class Server:
    """Represents an instance of an actionable rubybot class
    Arguments:
    client : A discord.client instance
    a      : A string, int, or discord.server.Server object
    Provides:
    server   : a discord.server.Server object
    member   : a discord.Member representing client's member in the server
    modroles : User-defined list of mod roles
    commands : A list of rubybot command instances"""

    def __init__(self, client, a):
        try:
            if str(type(a)) == "<class 'int'>":
                # nonlocal a
                a = str(a)
            if str(type(a)) == "<class 'str'>":
                # nonlocal a
                a = client.get_server(a)
            if str(type(a)) != "<class 'discord.server.Server'>":
                raise TypeError(a, 'Argument is not a discord server')
        except TypeError:
            raise
        self.server = a
        self.member = a.get_member(client.user.id)
        self.modroles = []
        self.commands = []
        servers.update({a.id: self})

    def add_cmd(self, c):
        if str(type(c)) == "<class 'rubybot_classes.Command'>":
            self.commands.append(c)
            self.commands = list(set(self.commands))
        else:
            raise TypeError(c, str(type(c)) +
                            " is not a rubybot command class!")

    def add_cmds(self, cs):
        for c in cs:
            self.add_cmd(c)
    def remove_cmds(self, cs):
        for c in cs:
            try:
                self.commands.remove(c)
            except Exception:
                pass
        self.commands = list(set(self.commands))
