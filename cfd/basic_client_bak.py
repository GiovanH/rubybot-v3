
from __future__ import print_function
import discord
from discord.ext import commands
import random
import traceback
import asyncio
import re
import urllib.request
import json
import os
import time
from time import gmtime, strftime
from datetime import datetime
import sys

class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

def eprint(*args, **kwargs):
	t = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print(t, file=sys.stderr, **kwargs)
	print(*args, file=sys.stderr, **kwargs)

description = '''An example client to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''

client = discord.Client()
token = 'MjQzMjczMDY4MTI5MTU3MTIw.CvslNg.7BCNEfVTd03zqmwHJdtEFIdOhoQ'
feedurl = 'http://loreweaver-universe.tumblr.com/'
lastPostID = '0'
mostRecentID = '1'
helpstr = "List of user commands:\n!rules\n!frog\n!roll NdN\n!roll NdN[ droplowest N] | [ - N] [ +N]\n\nList of admin commands:\n!bad @user\n!bad @user1 @user2...\n!frug @user\n!frug @user1 @user2...\n!frugnuke N\n!unbad @user\n!unbad @user1 user2...\n!help\n!restart\n\nList of PM commands:\nnone atm"
freq = 30
rulestxt = "**No politics, no porn, and no spoilers!**\n\nPlease keep discussion of things Lore hasn't seen yet to the spoilerchat! \n\nPlease don't push Lore on when he's doing an episode. It's stressful and unnecessary. Be polite! \n\n**Current important spoiler topics:** \n==No Undertale discussion *at all* outside the spoilerchat until he finishes the game\n==No Steven Universe past his latest liveblog\n==No Over the Garden Wall or Madoka Magica until he starts those liveblogs.\n if you're not certain about other things he could get spoiled on, go ahead and ask!\n\nPlease also keep all Homestuck talk to the Homestuck chat, as Minda is liveblogging it, and we all know how spoilery that can get.\n\nKeep nonsense-posting to The Pit, and **above all be excellent to each other.**"
#client.get_channel('243261625304481793')

#for message in client.logs_from(workingChan):
#	say(message.content)

r = urllib.request.urlopen("http://allaboutfrogs.org/funstuff/randomfrog.html").read()
r = r.decode()
regex = re.compile('"(http:\/\/www\.allaboutfrogs\.org\/funstuff\/random\/.*?)"')
froggos = regex.findall(r)

r = urllib.request.urlopen("http://stickyfrogs.tumblr.com/tagged/frogfriends").read()
r = r.decode()
regex = re.compile('img src="(.*?)"')
froggos.extend(regex.findall(r))

r = urllib.request.urlopen("https://twitter.com/stickyfrogs/media").read()
r = r.decode()
froggos.extend(re.compile('img data-aria-label-part src="(.*?)"').findall(r))

r = urllib.request.urlopen("https://twitter.com/Litoriacaeru/media").read()
r = r.decode()
froggos.extend(re.compile('img data-aria-label-part src="(.*?)"').findall(r))

froggos.extend(['https://i.reddituploads.com/938e4d7afef844598766444d14af1a6d?fit=max&h=1536&w=1536&s=9b30113694dcc47388f6e6f2fcc72b2e','https://pbs.twimg.com/media/C0BE7ayUQAABVWC.jpg','https://pbs.twimg.com/media/C2iX8kBVQAEmI65.jpg','https://pbs.twimg.com/media/CoXgucwVIAArMk6.jpg','https://pbs.twimg.com/media/C2vpipDUAAAkmRG.jpg','https://cdn.discordapp.com/attachments/232218346999775232/272703135753961482/4e4f4e53bf6845e080f17cbf1cd790e1.png','http://i3.kym-cdn.com/photos/images/original/001/157/712/77a.png','http://i3.kym-cdn.com/photos/images/original/001/157/712/77a.png','http://i3.kym-cdn.com/photos/images/original/001/157/712/77a.png','http://i3.kym-cdn.com/photos/images/original/001/157/712/77a.png','https://68.media.tumblr.com/c785cbf01b31413dbd11016b87e7ea2f/tumblr_okhxwbwgk81rhl4f0o3_540.png','https://68.media.tumblr.com/09085bda7aaf4a7c6f9e997cb69e6c96/tumblr_okhuu3CrMw1rhl4f0o1_1280.png','https://68.media.tumblr.com/09085bda7aaf4a7c6f9e997cb69e6c96/tumblr_okhuu3CrMw1rhl4f0o1_1280.png','https://68.media.tumblr.com/2b36852332d43ef5783daf083371036a/tumblr_oj8dn0q63Y1t1y79mo1_1280.jpg','https://pbs.twimg.com/media/C2Z3YxPUcAEYt03.jpg','http://68.media.tumblr.com/33515e6816c56fc76d8f0ba71d043f8b/tumblr_inline_odmrv9ymn01rkjj27_400.jpg','http://68.media.tumblr.com/a05b82de76eb7eb68e7bc36b7fdda489/tumblr_inline_odmrx6r6A21rkjj27_1280.jpg'])
print(froggos)
print(len(froggos))
eprint("started!")

#Initialization
@client.event
@asyncio.coroutine
def on_ready():
	global gio
	gio = yield from client.get_user_info('233017800854077441')
	
	global workingChan
	workingChan = client.get_channel('232218346999775232')
	
	global rubychan
	rubychan = client.get_channel('243542820189765633')
	
	global modchat
	modchat = client.get_channel('243461266687918081')
	
	global server
	server = client.get_server('232218346999775232')
	
	global rubybot_member
	rubybot_member = server.get_member('243273068129157120')
	yield from client.change_presence(game=discord.Game(name="with ur heart <3",type=1))
	
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')
	print(workingChan)
	print(rubychan)
	print('------')
	#yield from client.send_message(gio, "Can you hear me?")
	
	#gameplayed = MAIN.get("gameplayed", "github/freiheit/discord_rss_bot")
	#yield from client.change_status(game=discord.Game(name=gameplayed))
	
	loop = asyncio.get_event_loop()
	loop.create_task(background_check_feed(loop))



#IM GOING TO REPORT THIS
@client.event
@asyncio.coroutine
def on_message_edit(before, after):
	global gio
	fmt = '**{0.author}** edited their message from:\n{1.content}\nto\n{0.content}'
	print(fmt.format(after,before))
	# yield from client.send_message(gio, fmt.format(after, before))


@client.event
@asyncio.coroutine
def on_message_delete(message):
	global gio
	fmt = '{0.author.name} has deleted the message:\n{0.content}'
	print(fmt.format(message))
# yield from client.send_message(gio, fmt.format(message))


@asyncio.coroutine
def background_check_feed(asyncioloop):
	global timezone
	global workingChan
	global rubychan
	global freq
	
	
	# Basically run forever
	while not client.is_closed:
		# And tries to catch all the exceptions and just keep going
		# (but see list of except/finally stuff below)
		try:
			global mostRecentID
			global feedurl
			global lastPostID
			
			r = urllib.request.urlopen(feedurl).read()
			r = r.decode()
			#re.search('article', r)
			
			mostRecentID = re.search('article.* data-post-id="(.*)"', r).group(1)
			if mostRecentID != lastPostID:
				eprint(lastPostID + " -> " + mostRecentID)
				print(lastPostID + " -> " + mostRecentID)
				if '0' != lastPostID:
					print(mostRecentID)
					print("Update")
					print(lastPostID)
					yield from client.send_message(rubychan, "[[ " + "Update! http://loreweaver-universe.tumblr.com/post/" + mostRecentID + "/ ]]")
					yield from client.send_message(workingChan, "<:smolrubes:243554386549276672> [[ " + "Update!" + " ]]")
				
			lastPostID = mostRecentID
		except:
			print("error")
			raise
		# No matter what goes wrong, wait same time and try again
		finally:
			yield from asyncio.sleep(freq)


@asyncio.coroutine
def alias_peribot():
	fp = open("peribot.png", 'rb')
	filestream = fp.read()
	yield from client.edit_profile(avatar=filestream)
	fp.close()
	yield from client.change_nickname(rubybot_member, "Peribot")

@asyncio.coroutine
def alias_rubybot():
	fp = open("rubybot.png", 'rb')
	filestream = fp.read()
	yield from client.edit_profile(avatar=filestream)
	fp.close()
	yield from client.change_nickname(rubybot_member, "rubybot")

@asyncio.coroutine
def alias_sapphy():
	fp = open("sapphire.jpg", 'rb')
	filestream = fp.read()
	yield from client.edit_profile(avatar=filestream)
	fp.close()
	yield from client.change_nickname(rubybot_member, "sapphy")

@asyncio.coroutine
def alias_peribot():
	fp = open("peribot.png", 'rb')
	filestream = fp.read()
	yield from client.edit_profile(avatar=filestream)
	fp.close()
	yield from client.change_nickname(rubybot_member, "Peribot")

@asyncio.coroutine
def bad(target,source,channel):
	global rubybot_member
	global modchat
	if source == None:
		source = rubybot_member
	
	role = discord.utils.get(server.roles, id='242853719882858496')
	verified = discord.utils.get(server.roles, id='275764022547316736')	
	if role not in target.roles:
		yield from alias_peribot()
		yield from client.send_message(channel, target.name + " has been badded to the pit by " + source.name  + ".")
		yield from client.send_message(modchat, "Log: " + target.name + " has been badded to the pit by " + source.name )
	yield from client.send_message(target, "You are a bad frog." )
	yield from client.add_roles(target, role)
	try:
		yield from client.remove_roles(target, verified)
	except Exception:
		yield from client.send_message(modchat, "Verification error. Double check." )
		return
	yield from alias_rubybot()
	
@asyncio.coroutine
def unbad(target,source):
	global modchat
	role = discord.utils.get(server.roles, id='242853719882858496')
	verified = discord.utils.get(server.roles, id='275764022547316736')	
	try:
		yield from client.add_roles(target, verified)
	except Exception:
		yield from client.send_message(modchat, "Verification error. Double check." )
		return
	yield from client.remove_roles(target, role)
	yield from alias_sapphy()
	yield from client.send_message(workingChan, target.name + " has been unbadded by " + source.name)	
	yield from client.send_message(modchat, "Log: " + target.name + " has been unbadded by " + source.name )
	yield from alias_rubybot()	
			
def rollplain(rolls,limit):
	resultarray = [(random.randint(1, limit)) for r in range(rolls)]
	#result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
	resultarray.sort()
	return resultarray

def totalDelimitedList(list,number):
	total = 0

	#array2 = [int(i) for i in list.split(',')]	
	array2 = list
	array2.sort()
	print(array2)
	array2 = array2[number:]
	
	print(array2)
	
	for i in array2:
		total += i
	return total

@asyncio.coroutine
def rollcmd(dice,message):
	print(dice)
	bonus = 0
	drops = 0
	"""Rolls a dice in NdN format."""
	if "+" in dice: 
		try:
			dice,bonus = map(str, dice.split(' +'))
		except Exception:
			yield from client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N" )
			return
	if "droplowest" in dice: 
		try:
			dice,drops = map(str, dice.split(' droplowest '))
		except Exception:
			yield from client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N droplowest N" )
			return
	elif "-" in dice: 
		try:
			dice,drops = map(str, dice.split(' -'))
		except Exception:
			yield from client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N -N" )
			return
	try:
		rolls, limit = map(int, dice.split('d'))
	except Exception:
		yield from client.send_message(message.channel, "I don't understand that dice notation! The format is NdN" )
		return
		
	bonus = int(bonus)
	drops = int(drops)
	if rolls + limit > 200:
		yield from client.send_message(message.channel, "Hey, I'm really sorry " + message.author.mention + ", but I can't do that in my head. :c")
		return
	 
	try:
		result = rollplain(rolls,limit)
		resultsstr = ', '.join(str(result[r]) for r in range(rolls))
		if rolls > 1:
			total = totalDelimitedList(result,drops)
			yield from client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + "\nTotal: " + str(total) + "+ " + str(bonus) + " = " + str(total+bonus))
		else:
			yield from client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + " + " + str(bonus) + " = " + str(result[0]+bonus))
		
		
	except Exception:
		yield from client.send_message(message.channel, message.author.mention + "  :? " )
		return
	if ((rolls == 4) and (limit == 20)) or (rolls == 69) or (limit == 69):
		yield from client.send_message(message.channel, "you meme-loving degenerates.")


#Main reacion loop
@client.event
@asyncio.coroutine
def on_message(message):
	#print("" + message.author.name + ": " + message.content)
	#tic = time.clock()
	# we do not want the bot to react to itself
	if message.author == client.user:
		return
	
	global gio
	global server
	global rulestxt
	global workingChan
	global lastPostID
	global rubybot_member
	
	if message.server != None:
		print("[" + message.channel.name + "]" + message.author.name + ": " + message.clean_content)
		if message.content.startswith('!help'):
			yield from client.send_message(message.author, helpstr)
			yield from client.delete_message(message)
			
		if "rubybot" in message.content.lower():
			print("Debug: i've beem nentioned!")
			yield from client.add_reaction(message, ":smolrubes:243554386549276672")
			
		if "boobybot" in message.content.lower():
			print("Debug: i've beem nentioned!")
			yield from client.add_reaction(message, ":thatsmywife:244688656911171585")	
		
		if message.content.startswith('!verify'):
			if message.channel.permissions_for(message.author).manage_messages:	
				verified = discord.utils.get(server.roles, id='275764022547316736')	
				for member in message.mentions:					
					if verified not in member.roles:
						yield from client.add_roles(member, verified)
						yield from client.send_message(message.channel, "Verified user " + member.name) 
					else:
						yield from client.send_message(message.channel, "User is already verified: " + member.name) 
			yield from client.delete_message(message)
		
		# if message.author == server.get_member('233026647882727434'):
			# if "nut" in message.content.lower() or "nipple" in message.content.lower():
				# yield from client.delete_message(message)
				# yield from bad(message.author,None,message.channel)
		
		# if "bismuth" in message.content.lower() and message.channel == workingChan:
			# yield from client.delete_message(message)
			# yield from client.send_message(message.author, "You can't talk about bismuth yet!")
			# fmt = 'I had to delete {0.author.name}\'s message:\n{0.content}'
			# yield from client.send_message(client.get_channel('233018924562776064'), fmt.format(message))
		
		if message.channel == client.get_channel('245818265543114752'):
			if message.content.upper() != message.content:
				yield from client.delete_message(message)
				yield from client.send_message(message.author, "CAPS LOCK IS CRUISE CONTROL FOR COOL")
				yield from client.send_message(message.channel, "CAPS LOCK IS CRUISE CONTROL FOR COOL")
				yield from bad(message.author,None,message.channel)
		
		# if message.content.startswith('!callvote'):
			# msg = client.send_message(message.channel, 'React with thumbs up or thumbs down.')
			# yield from msg
			# res = client.wait_for_reaction(['👍', '👎'], message=msg)
			# yield from res
			# yield from client.send_message(message.channel, '{.user} reacted with {.reaction.emoji}!'.format(res))
		
		if message.content.startswith('!frog'):
			yield from client.send_typing(message.channel)
			global froggos
			frogi = (random.randint(1, len(froggos)))
			froggo = froggos[frogi]
			yield from client.send_message(message.channel, "[" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": " + froggo )
			yield from client.delete_message(message)
			
			
		if message.content.startswith('!rules'):
			yield from client.send_typing(message.channel)
			yield from client.send_message(message.channel, rulestxt)
			yield from client.delete_message(message)
		
			
		# if message.content.startswith('!love'):
			# yield from client.send_message(message.channel, "You both love me and I love both of you! <:smolrubes:243554386549276672>")
			# yield from client.delete_message(message)
		
		if message.content.startswith('!bad'):
			
			for m in message.mentions:
				#msg = message.content[5:]
				if message.channel.permissions_for(message.author).manage_messages and not message.channel.permissions_for(m).ban_members:
					target = m
				else:
					target = message.author
				if target == None:
					yield from client.send_message(message.channel, "No such person" )
					yield from client.delete_message(message)
					return
					
				yield from bad(target,message.author,message.channel)
			yield from client.delete_message(message)
		
		if message.content.startswith('!shadowbad'):
			
			for m in message.mentions:
				#msg = message.content[5:]
				if message.channel.permissions_for(message.author).manage_messages and not message.channel.permissions_for(m).ban_members:
					target = m
				else:
					target = message.author
				if target == None:
					yield from client.send_message(message.channel, "No such person" )
					yield from client.delete_message(message)
					return
					
				yield from bad(target,None,message.channel)
			yield from client.delete_message(message)
			
		if message.content.startswith('!unbad'):
			for m in message.mentions:
				if message.channel.permissions_for(message.author).manage_messages:
					#msg = message.content[7:]
					target = m
					
					if target == None:
						yield from client.send_message(message.channel, "No such person" )
						yield from client.delete_message(message)
						return
					yield from unbad(target,message.author)
			yield from client.delete_message(message)
		
		if message.content.startswith('!frug '):
			if message.channel.permissions_for(message.author).manage_messages:
				for m in message.mentions:
					target = m					
					if target == None:
						yield from client.send_message(message.channel, "No such person" )
						yield from client.delete_message(message)
						return
					yield from client.change_nickname(target, "frug")
				yield from client.delete_message(message)
		
		if message.content.startswith('!pm '):
			if message.channel.permissions_for(message.author).manage_messages:
				for m in message.mentions:
					target = m					
					if target == None:
						yield from client.send_message(message.channel, "No such person" )
						yield from client.delete_message(message)
						return
					
					print(message.content)
					content = message.content[27:]
					
					print(content)
					yield from client.send_message(target, content )
				yield from client.delete_message(message)
		if message.content.startswith('!restart'):
			if message.channel.permissions_for(message.author).manage_messages:
				yield from client.change_status(game=discord.Game(name="swords"))
				yield from client.delete_message(message)
				os.system("killall python3")  
		
		if message.content.startswith('!tippingfrog'):
			if message.channel.permissions_for(message.author).manage_messages:		
				role = discord.utils.get(server.roles, id='275764022547316736')	
				badr = discord.utils.get(server.roles, id='242853719882858496')
				for server in client.servers:
					for member in server.members:
						if role not in member.roles:
							yield from client.add_roles(member, role)
							yield from client.remove_roles(member, badr)
							yield from client.send_message(message.channel, "Verified user " + member.name) 
				yield from client.send_message(message.channel, "ribbit") 
		
		
		
		if message.content.startswith('!tippingpoint'):
			if message.channel.permissions_for(message.author).manage_messages:		
				table = "Member log: \n"
				for server in client.servers:
					for member in server.members:
						table += member.name
						table += "\t"
						table += str(member.joined_at)
						table += "\n"
				print(table)
				yield from client.send_message(message.channel, "```" + table + "```") 
			
		if message.content.startswith('!frugnuke '):
			if message.channel.permissions_for(message.author).manage_messages:
				msg = message.content[10:]
				print("Getting logs ")
				logs = yield from client.logs_from(message.channel, int(msg))
				
				print("Itterating  logs ")
				for logmessage in logs:
					 # python will convert \n to os.linesep
					#yield from client.send_message(gio, message.author.name)
					
					try:
						print("Targetting " + logmessage.author.name)
						yield from client.change_nickname(logmessage.author, "frug")
					except BaseException as e:
						print("error")
				
				yield from client.delete_message(message)
				
		if message.content.startswith('!roll'):# and message.channel == client.get_channel('240266528417775617'):
			dice = message.content[6:]
			
			yield from alias_peribot()
			yield from rollcmd(dice,message)
			yield from alias_rubybot()
				
	if message.server == None:
		print("PM [" + message.author.name + "]: " + message.content)
		if message.content.startswith('!help'):
			yield from client.send_message(message.author, helpstr)
			
		if message.author == gio:
			if message.content.startswith('!eval'):
				msg = message.content[6:]
				try:
					eval(msg)
				except BaseException as e:
					yield from client.send_message(message.author, str(e))
			if message.content.startswith('!roles'):
				for role in server.roles:
					yield from client.send_message(message.author, str(role.name)+": "+str(role.id))
			
			if message.content.startswith('!syseval'):
				msg = message.content[9:]
				try:
					os.system(msg)
				except BaseException as e:
					yield from client.send_message(message.author, str(e))
			if message.content.startswith('!say'):
				msg = message.content[5:]
				print(type(msg))
				yield from client.send_message(workingChan, msg)
			
			if message.content.startswith('!avatar'):
				msg = message.content[8:]
				fp = open(msg, 'rb')
				filestream = fp.read()
				yield from client.edit_profile(avatar=filestream)
				fp.close()
				
			if message.content.startswith('!nick'):
				nickname = message.content[6:]
				yield from client.change_nickname(rubybot_member, nickname)
				
				
			if message.content.startswith('!smol'):
				print("sending one smol")
				yield from client.send_message(workingChan, "<:smolrubes:243554386549276672>")
				
			if message.content.startswith('!fakeupdate'):
				lastPostID = '1'
				
			if message.content.startswith('!updebug'):
				r = urllib.request.urlopen(feedurl).read()
				r = r.decode()
				#re.search('article', r)
				mostRecentID = re.search('article.* data-post-id="(.*)"', r).group(1)
				yield from client.send_message(message.author, "```" + str(lastPostID) + "/" + str(mostRecentID) + "```")
			
			if message.content.startswith('!peribot'):
				yield from alias_peribot()	
			if message.content.startswith('!rubybot'):
				yield from alias_rubybot()	
			if message.content.startswith('!sapphire'):
				yield from alias_sapphy()
			
			if message.content.startswith('!chan'):
				msg = message.content[6:]
				workingChan = client.get_channel(msg)
				yield from client.send_message(message.author, workingChan.name)
				
			
			if message.content.startswith('!emoji'):
				for s in client.get_server('232218346999775232').emojis:
					print(s)
					#yield from client.send_message(workingChan, "<:smolrubes:243554386549276672>")
				
			if message.content.startswith('!log'):
				logno = int(message.content[5:])
				for channel in server.channels:
					logs = yield from client.logs_from(channel, logno)
					f = open('/media/bluebook/logs/' + channel.name + '.log','w')
					yield from client.send_message(message.author, "Logged " + channel.name)
					for message in logs:
						f.write(str(message.timestamp) + " " + message.author.name + ": " + message.content + ' ' + json.dumps(message.attachments) + '\n') # python will convert \n to os.linesep
					f.close()
				print("done")

	#toc = time.clock()
	#print("Message processing time: " + str(toc - tic))
	
client.run(token)
