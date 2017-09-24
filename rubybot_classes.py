import discord
from discord.ext import commands

class Command:
    """A simple example class"""
    def __init__(self):
      self.data = []

class Server:
    """A simple example class"""
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
