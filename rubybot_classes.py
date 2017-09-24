import discord
from discord.ext import commands

class Command:
    """A simple example class"""
    def __init__(self,cb,permlevel):
      self.data = []

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
    def __init__(self,client,a):
        try:
            if str(type(a)) == "<class 'int'>":
                #nonlocal a
                a = str(a)
            if str(type(a)) == "<class 'str'>":
                #nonlocal a
                a = client.get_server(a)
            if str(type(a)) != "<class 'discord.server.Server'>":
                raise TypeError(a,'Argument is not a discord server')
        except TypeError:
            raise
        self.server = a
        self.member = a.get_member(client.user.id)
        self.modroles = []
        self.commands = []

    def add_cmd(self,c):
        if str(type(c)) == "<class 'rubybot_classes.Command'>":
            self.commands.append(c)
        else:
            raise TypeError(c,str(type(c)) + " is not a rubybot class!")
