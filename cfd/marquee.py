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
	server_lwu = rbot.Server(client, 232218346999775232)
	loop = asyncio.get_event_loop()
	loop.create_task(marquee(3))

nickname = "Rubybot! FEEL THE SPEED "
async def marquee(freq):
	#global timezone
	global nickname
	while not client.is_closed:
		#print(nickname)
		nickname = nickname[2:] + nickname[0:2]
		print(nickname)
		await client.change_nickname(rbot.Server(client, 232218346999775232).member, "<" + nickname[:12] + "<")
		await asyncio.sleep(freq)

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
