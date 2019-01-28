#!python3

import discord
from discord.ext import commands
import random
import traceback
import asyncio
import re
import pickle
import urllib.request
import json
import os
import time
from time import gmtime, strftime
import datetime
import sys
import rubybot_classes as rbot

async def send_message_smart(dest,msg):
	m = ""
	for line in msg.split('\n'):
		m += line + "\n"
		if len(m) >= 1600:
			await client.send_message(dest, m)
			m = ""
	await client.send_message(dest, m)

def eprint(*args, **kwargs):
	#global gio
	t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	# print(t, file=sys.stderr, **kwargs)
	# print(*args, file=sys.stderr, **kwargs)
	print("[Logging:]" + t)
	print(*args, **kwargs)
	# await client.send_message(gio, *args)


def pickleLoad(filename):
	filehandler = open("pickle/" + filename + ".obj", 'rb')
	object = pickle.load(filehandler)
	return object


def pickleSave(object, filename):
	filehandler = open("pickle/" + filename + ".obj", 'wb')
	pickle.dump(object, filehandler)

client = discord.Client()

froggos = ["Not ready yet! Try again!"]

async def loadfrogs():
	global froggos
	froggos = []
	with open('frogs.frog') as f:
		for line in f:
			froggos.append(line[:-1])
	try:
		r = urllib.request.urlopen(
			"http://allaboutfrogs.org/funstuff/randomfrog.html").read()
		r = r.decode()
		regex = re.compile(
			'"(http:\/\/www\.allaboutfrogs\.org\/funstuff\/random\/.*?)"')
		froggos.extend(regex.findall(r))
	except:
		traceback.print_exc(file=sys.stdout)
		eprint("frog error, continuing")
	try:
		r = urllib.request.urlopen(
			"http://stickyfrogs.tumblr.com/tagged/frogfriends").read()
		r = r.decode()
		regex = re.compile('img src="(.*?)"')
		froggos.extend(regex.findall(r))
	except:
		traceback.print_exc(file=sys.stdout)
		eprint("frog error, continuing")
	try:
		r = urllib.request.urlopen(
			"https://twitter.com/stickyfrogs/media").read()
		r = r.decode()
		froggos.extend(re.compile(
			'img data-aria-label-part src="(.*?)"').findall(r))
	except:
		traceback.print_exc(file=sys.stdout)
		eprint("frog error, continuing")
	try:
		r = urllib.request.urlopen(
			"https://twitter.com/Litoriacaeru/media").read()
		r = r.decode()
		froggos.extend(re.compile(
			'img data-aria-label-part src="(.*?)"').findall(r))
	except:
		traceback.print_exc(file=sys.stdout)
		eprint("frog error, continuing")
	froggos = list(set(froggos))
	frogfile = 'frogs.frog'
	uniqlines = open(frogfile).readlines()
	for frog in froggos:
		uniqlines.insert(0, frog + "\n")
	open(frogfile, 'w').writelines(set(uniqlines))

# Initialization
def logpath(message):
	"""Given a message, returns a filepath for logging that message."""
	if message.server != None:
		_dir = "logs/" + message.channel.server.name + "/" + message.channel.name
	else:
		_dir = "logs/direct_messages/" + message.author.name
	try:
		os.makedirs(_dir)
	except:
		pass
	return _dir + "/" + str(datetime.date.today()) + ".log"

@client.event
async def on_ready():
	await client.change_presence(game=discord.Game(name="with ur heart <3", type=1))

	global gio
	gio = await client.get_user_info('233017800854077441')

	await loadfrogs()
	try:
		with open("last_trace.log", "r") as tracefile:
			await client.send_message(gio, "April fools just came online. Last error: \n" + tracefile.read())
		with open("git.log", "r") as _file:
			await client.send_message(gio, "Latest git revision: \n" + _file.read())
		with open("last_trace.log", 'w', newline='\r\n') as tracefile2:
			tracefile2.write(
				"Nothing known! No exception written to file!")
			tracefile2.flush()
	except:
		pass

async def cmd_frog_func(message):
	await client.send_typing(message.channel)
	print(len(froggos))
	frogi = random.randint(1, len(froggos))
	froggo = froggos[frogi-1]
	await client.send_message(message.channel, "[" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": " + froggo)
	await client.send_message(gio, "Sent frog in channel "+ str(message.channel.name) +" [" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": <" + froggo + ">")
	return

global frogprob
frogprob = 400

@client.event
async def on_message(message):
	global frogprob
	#tic = time.clock()
	# we do not want the bot to react to itself
	if message.author == client.user:
		return
	
	if message.content.lower().startswith('!' + "getfrogprob") and message.author == gio:
		await client.send_message(message.author, "One in " + str(frogprob))
	if message.content.lower().startswith('!' + "setfrogprob") and message.author == gio:
		try:
			frogprob = int("".join(message.content.split()[1:]))
			await client.send_message(message.author, "Frogprob is now One in " + str(frogprob))
		except BaseException as e:
			await client.send_message(message.author, "Error!")
		await client.change_presence(game=discord.Game(name="with ur heart <" + str(100/float(frogprob)), type=1))
		
	if random.randint(0,frogprob) == 0:
		await cmd_frog_func(message)

with open("token", 'rb') as filehandler:
	token = pickle.load(filehandler)

while True:
	try:
		eprint("Running client")
		client.run(token)
		eprint("Successful completion?")
	except RuntimeError as e:
		eprint("Major fault - Runtime error")
		tb = traceback.format_exc()
		tb = tb + "\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		eprint(tb)
		with open("last_trace.log", "w") as f:
			f.write(tb)
			f.flush()
		break
	except SystemExit as e:
		eprint("Exiting peacefully")
		break
	except BaseException as e:
		eprint("Major fault - unknown cause")
		tb = traceback.format_exc()
		tb = tb + "\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		eprint(tb)
		with open("last_trace.log", "w") as f:
			f.write(tb)
			f.flush()
		# break

eprint("Program terminated: Ran over edge of file")
