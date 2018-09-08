import discord
# from discord.ext import commands

import hashlib
import requests

gio_id = '233017800854077441'

permissions = {}
servers = {}
commands = {}
direct_commands = {}


def permissionLevel(user, server):
    plvl = 0
    if user.id == gio_id:
        return 3
    if server is None:
        return plvl
    for r in user.roles:
        rlvl = permissions.get(server.id).get(r.id)
        if rlvl is None:
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
        if message.content.lower().startswith('!' + self.name.lower()):
            if permissionLevel(message.author, message.server) >= self.permlevel:
                await self.function(message)
            else:
                e = 'User ' + message.author.name + \
                    ' has insufficient permissions to perform command ' + self.name
                print(e)
                raise NameError(e)


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
            if isinstance(a, int):
                # nonlocal a
                a = str(a)
            if isinstance(a, str):
                # nonlocal a
                a = client.get_server(a)
            if not isinstance(a, discord.server.Server):
                raise TypeError(a, 'Argument is not a discord server')
        except TypeError:
            raise
        self.server = a
        self.member = a.get_member(client.user.id)
        self.modroles = []
        self.commands = []
        servers.update({a.id: self})

    def add_cmd(self, c):
        if isinstance(c, Command):
            self.commands.append(c)
            self.commands = list(set(self.commands))
        else:
            raise TypeError(c, str(type(c)) + " is not a rubybot command!")

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


class Frog:
    """Represents a frog."""

    def __init__(self, data):
        self.data = data
        self.checkmd5()

    def checkmd5(self):
        if self.data.get('md5') is not None:
            return
        try:
            req = requests.get(self.data['url'])
        except requests.exceptions.MissingSchema:
            raise
        hashm = hashlib.sha256
        self.data['md5'] = hashm(req._content).hexdigest()
        print(self.data['md5'])

    def __eq__(self, other):
        return self.data['md5'] == other.data['md5']

    def __hash__(self):
        return hash(self.data['md5'])
