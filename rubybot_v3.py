from __future__ import print_function
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

#TODO: Make sure all image assets point to the asset folder
#TODO: Modular command system


class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream

    def write(self, data):
        self.stream.write(data)
        self.stream.flush()

    def __getattr__(self, attr):
        return getattr(self.stream, attr)


sys.stdout = Unbuffered(sys.stdout)
sys.stderr = Unbuffered(sys.stderr)


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



#TODO: Load tokens from file instead
client = discord.Client()
helpstr = "Generic commands:\n```!rules\n!frog\n!callvote option1, option2[, option3...]\n!roll NdN\n!roll NdN[ droplowest N] | [ - N] [ +N]\n!help```\nAdmin:\n```!restart```\nLoreweaver Universe commands:\n```!pronoun [F|M|T|He|She|They|Him|Her|Them|Other] (This is a toggle!)\n!rules```\nAdmin:\n```!bad @user [@user2...]\n!shadowbad @user [@user2...]\n!frug @user [@user2...]\n!frugnuke N\n!unbad @user\n!unbad @user1 [user2...]\n!verify @user1 [user2...]```\nMinda Chat Commands:\nNone.\nTaboo commands:\n```!sortinghat```\nAdmin:\n```!reteam\n!unteam```\nList of PM commands:\n```!help```"
rulestxt = "**No politics, no porn, and no spoilers!**\n\nPlease keep discussion of things Lore hasn't seen yet to the spoilerchat! \n\nPlease don't push Lore on when he's doing an episode. It's stressful and unnecessary. Be polite! \n\n**Current important spoiler topics:** \n==No Undertale discussion *at all* outside the spoilerchat until he finishes the game\n==No Steven Universe past his latest liveblog\n==No Over the Garden Wall or Madoka Magica until he starts those liveblogs.\n if you're not certain about other things he could get spoiled on, go ahead and ask!\n\nPlease also keep all Homestuck talk to the Homestuck chat, as Minda is liveblogging it, and we all know how spoilery that can get.\n\nKeep nonsense-posting to The Pit, and **above all be excellent to each other.**"
# client.get_channel('243261625304481793')

# for message in client.logs_from(workingChan):
#	say(message.content)

global froggos
froggos = ["Not ready yet! Try again!"]

#@client.event


async def loadfrogs():
    global froggos
    froggos = []
    with open('frogs.frog') as f:
        for line in f:
            # print(line[:-1])
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


# print(froggos)
eprint("Parsing rubybot core routines")

# Initialization

def logpath(message):
    if message.server != None:
        _dir = "~/logs/" + message.channel.server.name + "/" + message.channel.name
    else:
        _dir = "~/logs/direct_messages/" + message.author.name
    try:
        os.makedirs(_dir)
    except:
        pass
    return _dir + "/" + str(datetime.date.today()) + ".log"

@client.event
async def on_ready():
    print('Initializing rubybot listeners')
    global gio
    gio = await client.get_user_info('233017800854077441')

    global workingChan
    workingChan = client.get_channel('232218346999775232')

    global modchat
    modchat = client.get_channel('243461266687918081')

    global lwu_server
    lwu_server = client.get_server('232218346999775232')

    global taboo_server
    taboo_server = client.get_server('245789672842723329')

    global taboo_teams
    taboo_teams = []
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='246194661763317761'))  # red team
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='246194717946019840'))  # blue team
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='246194772253999104'))  # wildcats
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='246194825370533889'))  # the real illuminati
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='246194907302199296'))  # cool and new team
    taboo_teams.append(discord.utils.get(taboo_server.roles,
                                         id='254164527271247872'))  # number one

    global minda_server
    minda_server = client.get_server('290270624558088192')

    global rubybot_member
    rubybot_member = lwu_server.get_member('243273068129157120')
    await client.change_presence(game=discord.Game(name="with ur heart <3", type=1))
    # await client.change_presence(game=discord.Game(name="[gio pls add meme]",type=1))

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    print(workingChan)
    print('------')
    # await client.send_message(gio, "Can you hear me?")
    #gameplayed = MAIN.get("gameplayed", "github/freiheit/discord_rss_bot")
    # await client.change_status(game=discord.Game(name=gameplayed))

    print("Creating event loops")
    loop = asyncio.get_event_loop()
    loop.create_task(background_check_feed(loop, 'http://loreweaver-universe.tumblr.com/',
                                           client.get_channel('232218346999775232'), client.get_channel('243542820189765633'), 90))
    loop.create_task(background_check_feed(loop, 'http://mindareadsoots.tumblr.com/',
                                           client.get_channel('290270624558088192'), client.get_channel('298828535894769665'), 90))
    loop.create_task(fear_of_death(1800))

    print("Defining localization enumerations")
    global emotes
    emotes = dict()
    emotes.update({minda_server: ':smolrubes:300822291229442048',
                   lwu_server: ':smolrubes:243554386549276672'})

    global blushemote
    blushemote = dict()
    blushemote.update({minda_server: ':smolrubes:300822291229442048',
                       lwu_server: ':thatsmywife:244688656911171585'})

    global modrole
    modrole = dict()
    modrole.update({minda_server:  discord.utils.get(minda_server.roles, id='298390405169283072'),
                    lwu_server: discord.utils.get(lwu_server.roles, id='282703165269213184')})
    print("Only frogs now")
    await loadfrogs()
    print("Fully loaded.")

# IM GOING TO REPORT THIS


@client.event
async def on_message_edit(before, after):
    message = after
    fmt = '**{0.author}** edited their message from: |{1.content}| to |{0.content}|\n'
    with open(logpath(message), 'a+') as file:
        file.write(fmt.format(after, before))
        file.write("[" + message.channel.name +"] " + message.author.name + ": " + message.clean_content + "\n")

    # await client.send_message(gio, fmt.format(after, before))


@client.event
async def on_message_delete(message):
    fmt = '{0.author.name} has deleted the message: |{0.content}|\n'
    with open(logpath(message), 'a+') as file:
        file.write(fmt.format(message))
        file.write("[" + message.channel.name +"] " + message.author.name + ": " + message.clean_content + "\n")

# await client.send_message(gio, fmt.format(message))


@client.event
async def on_member_join(member):
    if member.server is taboo_server:
        eprint("setting manual team")
        target = member
        newteam = random.choice(taboo_teams)
        await client.add_roles(target, newteam)
        for role in taboo_teams:
            # await client.send_message(message.channel, "Checking role " + role.name)
            if (role in target.roles) and (role is not newteam):
                # await client.send_message(message.channel, "Removing role " + role.name)
                await client.remove_roles(target, role)
        await client.send_message(member.server.default_channel, "Please welcome " + target.mention + " to " + newteam.name)


async def fear_of_death(freq):
    global timezone
    while not client.is_closed:
        # os.system("date >> ping.log")
        # os.system("ping discordapp.com -c 1 >> ping.log")

        os.system("rm kill.sh 2>> /dev/null")
        await asyncio.sleep(freq)


async def background_check_feed(asyncioloop, feedurl, workingChan, rubychan, freq):
    global timezone
    mostRecentID = '1'
    lastPostID = '0'
    # Basically run forever
    while not client.is_closed:
        # And tries to catch all the exceptions and just keep going
        # (but see list of except/finally stuff below)
        try:
            r = urllib.request.urlopen(feedurl).read()
            r = r.decode()
            mostRecentID = re.search(
                'article.* data-post-id="(.*)"', r).group(1)
            if mostRecentID != lastPostID:
                eprint(lastPostID + " -> " + mostRecentID)
                print(lastPostID + " -> " + mostRecentID)
                if '0' != lastPostID:
                    print(mostRecentID)
                    print("Update")
                    print(lastPostID)
                    await client.send_message(rubychan, "[[ " + "Update! " + feedurl + "post/" + mostRecentID + "/ ]]")
                    # await client.send_message(workingChan, "<" + emotes[workingChan.server] + "> [[ " + "Update! (" + lastPostID + " -> " + mostRecentID + ") ]]")
                    await client.send_message(workingChan, "<" + emotes[workingChan.server] + "> [[ Update! ]]")
            lastPostID = mostRecentID
        except:
            eprint("error fetching status for " + feedurl)
            # raise
        # No matter what goes wrong, wait same time and try again
        finally:
            await asyncio.sleep(freq)


async def alias_peribot():
    # fp = open("peribot.png", 'rb')
    # filestream = fp.read()
    # await client.edit_profile(avatar=filestream)
    # fp.close()
    await client.change_nickname(rubybot_member, "Peribot")


async def alias_rubybot():
    # fp = open("rubybot.png", 'rb')
    # filestream = fp.read()
    # await client.edit_profile(avatar=filestream)
    # fp.close()
    await client.change_nickname(rubybot_member, "rubybot")


async def alias_sapphy():
    # fp = open("sapphire.jpg", 'rb')
    # filestream = fp.read()
    # await client.edit_profile(avatar=filestream)
    # fp.close()
    await client.change_nickname(rubybot_member, "sapphy")


async def alias_peribot():
    # fp = open("peribot.png", 'rb')
    # filestream = fp.read()
    # await client.edit_profile(avatar=filestream)
    # fp.close()
    await client.change_nickname(rubybot_member, "Peribot")

# ismod boolean (modrole[message.server] in user.roles)


async def bad(target, source, channel):
    global rubybot_member
    global modchat
    if source == None:
        source = rubybot_member

    badr = discord.utils.get(lwu_server.roles, id='242853719882858496')
    verified = discord.utils.get(lwu_server.roles, id='275764022547316736')

    i = 1
    while (badr not in target.roles):
        i = i + 1
        await client.add_roles(target, badr)
    while (verified in target.roles):
        i = i + 1
        await client.remove_roles(target, verified)
    # if verified in target.roles:
        # eprint("unverifying")
        # await client.remove_roles(target, verified)
    # else:
        # eprint("Already unverified?")
        # await client.send_message(modchat, "For unknown reasons, badding may not have removed verified frogs role. Please check. ")

    # if badr not in target.roles:
        # eprint("badding")
        # await client.add_roles(target, badr)
    # else:
        # eprint("Already bad?")

    await alias_peribot()
    await client.send_message(channel, target.name + " has been badded to the pit by " + source.name + ".")
    await client.send_message(modchat, "Log: " + target.name + " has been badded to the pit by " + source.name)
    # await client.send_message(target, "You have been a bad frog." )

    await alias_rubybot()


async def unbad(target, source):
    global modchat
    badr = discord.utils.get(lwu_server.roles, id='242853719882858496')
    verified = discord.utils.get(lwu_server.roles, id='275764022547316736')

    # await client.remove_roles(target, badr)
    i = 1
    while (badr in target.roles):
        i = i + 1
        await client.remove_roles(target, badr)
    while (verified not in target.roles):
        i = i + 1
        await client.add_roles(target, verified)

    # if badr in target.roles:
        # await client.remove_roles(target, badr)
    # else:
        # eprint("Already unbadded?")

    # if verified not in target.roles:
        # await client.add_roles(target, verified)
    # else:
        # eprint("Already verified?")

    await alias_sapphy()
    # await client.send_message(workingChan, target.name + " has been unbadded by " + source.name)
    await client.send_message(modchat, "Log: " + target.name + " has been unbadded by " + source.name + ".")
    await alias_rubybot()


def rollplain(rolls, limit):
    resultarray = [(random.randint(1, limit)) for r in range(rolls)]
    #result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    resultarray.sort()
    return resultarray


def totalDelimitedList(list, number):
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


async def rollcmd(dice, message):
    print(dice)
    bonus = 0
    drops = 0
    """Rolls a dice in NdN format."""
    if "+" in dice:
        try:
            dice, bonus = map(str, dice.split(' +'))
        except Exception:
            await client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N")
            return
    if "droplowest" in dice:
        try:
            dice, drops = map(str, dice.split(' droplowest '))
        except Exception:
            await client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N droplowest N")
            return
    elif "-" in dice:
        try:
            dice, drops = map(str, dice.split(' -'))
        except Exception:
            await client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N -N")
            return
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.send_message(message.channel, "I don't understand that dice notation! The format is NdN")
        return

    bonus = int(bonus)
    drops = int(drops)
    if rolls + limit > 200:
        await client.send_message(message.channel, "Hey, I'm really sorry " + message.author.mention + ", but I can't do that in my head. :c")
        return

    try:
        result = rollplain(rolls, limit)
        resultsstr = ', '.join(str(result[r]) for r in range(rolls))
        if rolls > 1:
            total = totalDelimitedList(result, drops)
            await client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + "\nTotal: " + str(total) + "+ " + str(bonus) + " = " + str(total + bonus))
        else:
            await client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + " + " + str(bonus) + " = " + str(result[0] + bonus))

    except Exception:
        await client.send_message(message.channel, message.author.mention + "  :? ")
        return
    if ((rolls == 4) and (limit == 20)) or (rolls == 69) or (limit == 69):
        await client.send_message(message.channel, "you meme-loving degenerates.")


def isMod(server, member):
    global gio
    global modrole
    #eprint("checking mod status of " + member.name + " on " + server.name)
    # eprint(member.id)
    # eprint(gio.id)
    if (member.id == gio.id):
        #eprint("gio override, all hail")
        return True
    ismod = (modrole[server] in member.roles)
    # eprint(ismod)
    return ismod

# Main reacion loop


@client.event
async def on_message(message):
    #print("" + message.author.name + ": " + message.content)
    #tic = time.clock()
    # we do not want the bot to react to itself
    if message.author == client.user:
        return

    global gio
    global server
    global rulestxt
    global workingChan
    #global lastPostID
    global rubybot_member
    global lwu_server

    global taboo_server
    global taboo_teams

    global emotes
    global blushemote

    # if message.server != None:

    if message.server != None:  # Generic Server
        with open(logpath(message), 'a+') as file:
            file.write("[" + message.channel.name +"] " + message.author.name + ": " + message.clean_content + "\n")
        #print("[" + message.channel.server.name + "]\t" + )
        if message.content.startswith('!frog refresh') and isMod(message.server, message.author):
            await loadfrogs()
            await client.delete_message(message)
            return
        if message.content.startswith('!error'):
            m = [1]
            print(m[3])

        if message.content.startswith('!react'):
            msg = await client.send_message(message.channel, 'React to me')
            res = await client.wait_for_reaction(message=msg)
            await client.send_message(message.channel, '{0.reaction.emoji} {0.reaction.emoji.id} {0.reaction.emoji.name} {0.reaction.emoji.url}!'.format(res))

        if message.content.startswith('!strawpoll') or message.content.startswith('!callvote'):
            reaction_dict = random.choice(
                ['🇦🇧🇨🇩🇪🇫🇬🇭', '❤💛💚💙💜🖤💔', '🐶🐰🐍🐘🐭🐸', '🍅🍑🍒🍌🍉🍆🍓🍇'])
            # reaction_dict = random.choice(['🇦🇧🇨🇩🇪🇫🇬🇭', '💛💚💙💜🖤💔','🐶🐰🐍🐘🐭🐸🐿',🍅🍑🍒🍌🍉🍆🍓🍇'])

            msg = ' '.join(message.content.split()[1:])  # Remove first word
            options = msg.split(', ')  # Create list from CSV
            pollmsg = await client.send_message(message.channel, "Loading...")
            i = 0
            polltext = message.author.name + " has called a vote:"
            for o in options:
                polltext = polltext + "\n" + reaction_dict[i] + ": " + o
                await client.add_reaction(pollmsg, reaction_dict[i])
                i = i + 1
            await client.edit_message(pollmsg, new_content=polltext)

        if message.content.startswith('!roles'):
            for role in message.server.roles:
                await client.send_message(message.author, str(role.name) + ": " + str(role.id))

        if message.content.startswith('!serverdata'):
            await client.send_message(message.author, message.server.name)
            await client.send_message(message.author, message.server.id)
            await client.send_message(message.author, message.server.icon)
            await client.delete_message(message)
            return

        if message.content.startswith('!sayhere'):
            msg = message.content[9:]
            print(type(msg))
            await client.send_message(message.channel, msg)
            await client.delete_message(message)
            return

        if message.content.startswith('!frog') or message.content.startswith('!contraband'):
            await client.send_typing(message.channel)
            global froggos
            frogi = (random.randint(1, len(froggos) - 1))
            froggo = froggos[frogi]
            #froggo = random.choice(froggos)
            await client.send_message(message.channel, "[" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": " + froggo)
            await client.delete_message(message)
            return
        elif message.content.startswith('!addfrog '):
            msg = message.content[9:]
            eprint("trying to add " + msg)
            if isMod(message.server, message.author):
                frogfile = 'frogs.frog'
                try:
                    urllib.request.urlopen(msg).read()
                except (urllib.error.HTTPError, urllib.error.URLError) as e:
                    await client.send_message(message.channel, "Check failed! Bad link? Details in log. Ignore this message if the link came from discord, or if the image shows up anyway.")
                    traceback.print_exc(file=sys.stdout)
                    # return
                fh = open(frogfile, 'a')
                fh.write(msg + "\n")
                froggos.extend(msg)
                uniqlines = set(open(frogfile).readlines())
                open(frogfile, 'w').writelines(set(uniqlines))
                await loadfrogs()
                await client.send_message(message.channel, "Added frog.")
            else:
                await client.send_message(message.channel, "You do not have permissions to add a frog!")
        # if message.content.startswith('!love'):
            # await client.send_message(message.channel, "You both love me and I love both of you! <:smolrubes:243554386549276672>")
            # await client.delete_message(message)

        if message.content.startswith('!emoji'):
            for s in message.server.emojis:
                await client.send_message(message.author, s.name + ", " + s.id)

        if message.content.startswith('!pm '):
            if (modrole[message.server] in message.author.roles):
                for m in message.mentions:
                    target = m
                    if target == None:
                        await client.send_message(message.channel, "No such person")
                        await clientF.delete_message(message)
                        return
                    print(message.content)
                    content = message.content[27:]
                    print(content)
                    await client.send_message(target, content)
                await client.delete_message(message)
            return

        if message.content.startswith('!restart') or message.content.startswith('!reload'):
            if isMod(message.server, message.author):
                await client.change_presence(game=discord.Game(name="swords", type=1))
                await client.delete_message(message)
                os.system("killall python3")
            return
        if message.content.startswith('!permissions'):
            eprint("!permissions called")
            if isMod(message.server, message.author):
                await client.send_message(message.channel, "Administrator")
            else:
                await client.send_message(message.channel, "User")
            return

        # and message.channel == client.get_channel('240266528417775617'):
        if message.content.startswith('!roll'):
            dice = message.content[6:]
            await alias_peribot()
            await rollcmd(dice, message)
            await alias_rubybot()
            return

        if "rubybot" in message.content.lower():
            print("Debug: i've beem nentioned!")
            await client.add_reaction(message, emotes[message.server])
            return

        if "boobybot" in message.content.lower():
            print("Debug: i've beem nentioned!")
            await client.add_reaction(message, blushemote[message.server])
            return

    if message.server == taboo_server:
        if message.content.startswith('!reteam') and isMod(message.server, message.author):
            eprint("setting manual team")
            for target in message.mentions:
                newteam = random.choice(taboo_teams)
                await client.add_roles(target, newteam)
                for role in taboo_teams:
                    # await client.send_message(message.channel, "Checking role " + role.name)
                    if (role in target.roles) and (role is not newteam):
                        # await client.send_message(message.channel, "Removing role " + role.name)
                        await client.remove_roles(target, role)
                await client.send_message(message.channel, "Please welcome " + target.mention + " to " + newteam.name)
            await client.delete_message(message)
        elif message.content.startswith('!unteam') and isMod(message.server, message.author):
            eprint("unsetting manual team")
            for target in message.mentions:
                for role in taboo_teams:
                    if (role in target.roles):
                        await client.remove_roles(target, role)
            await client.delete_message(message)
        elif message.content.startswith('!sortinghat'):
            await client.send_message(message.channel, "I will now determine your alignment.")
            target = message.author
            newteam = random.choice(taboo_teams)
            for role in taboo_teams:
                # await client.send_message(message.channel, "Checking role " + role.name)
                if (role in target.roles):
                    await client.send_message(message.channel, "It is too late. The die has been cast.")
                    return
            await client.add_roles(target, newteam)
            await client.send_message(message.channel, "Please welcome " + target.mention + " to " + newteam.name)

    if message.server == lwu_server:

        if message.content.startswith('!rules'):
            await client.send_typing(message.channel)
            await client.send_message(message.channel, rulestxt)
            await client.delete_message(message)
            return

        if message.content.startswith('!pins'):
            await client.send_typing(message.channel)
            pins = await client.logs_from(client.get_channel('278819870106451969'), limit=400)
            pinmsg = random.choice(list(pins))
            pinurl = pinmsg.content
            print(pinmsg.timestamp)
            for a in pinmsg.attachments:
                pinurl += "\n" + a.get('url')
            await client.send_message(message.channel, "Pin from " + pinmsg.author.name + " from " + str(pinmsg.timestamp) + ": " + pinurl)
            await client.delete_message(message)
            return

        if message.content.startswith('!bad'):
            for m in message.mentions:
                #msg = message.content[5:]
                if (modrole[message.server] in message.author.roles) and not message.channel.permissions_for(m).ban_members:
                    target = m
                else:
                    target = message.author
                if target == None:
                    await client.send_message(message.channel, "No such person")
                    await client.delete_message(message)
                    return
                await bad(target, message.author, message.channel)
            await client.delete_message(message)
            return

        if message.content.startswith('!shadowbad'):
            for m in message.mentions:
                #msg = message.content[5:]
                if (modrole[message.server] in message.author.roles) and not message.channel.permissions_for(m).ban_members:
                    target = m
                else:
                    target = message.author
                if target == None:
                    await client.send_message(message.channel, "No such person")
                    await client.delete_message(message)
                    return
                await bad(target, None, message.channel)
            await client.delete_message(message)
            return

        if message.content.startswith('!unbad'):
            for m in message.mentions:
                if (modrole[message.server] in message.author.roles):
                    #msg = message.content[7:]
                    target = m
                    if target == None:
                        await client.send_message(message.channel, "No such person")
                        await client.delete_message(message)
                        return
                    await unbad(target, message.author)
            await client.delete_message(message)
            return

        if message.content.startswith('!frug '):
            if (modrole[message.server] in message.author.roles):
                for m in message.mentions:
                    target = m
                    if target == None:
                        await client.send_message(message.channel, "No such person")
                        await client.delete_message(message)
                        return
                    await client.change_nickname(target, "frug")
                await client.delete_message(message)
            return

        if message.content.startswith('!pronoun'):
            pronoun = message.content[9:]
            #eprint("pronoun: " + pronoun);
            r_him = discord.utils.get(
                lwu_server.roles, id='285628551229603841')
            r_her = discord.utils.get(
                lwu_server.roles, id='285628637045063680')
            r_they = discord.utils.get(
                lwu_server.roles, id='285628689876647937')

            if ((pronoun.upper() == "HIM") or (pronoun.upper() == "HE") or (pronoun.upper() == "MALE") or (pronoun.upper() == "MAN") or (pronoun.upper() == "M") or (pronoun.upper() == "H")):
                role = r_him
            if ((pronoun.upper() == "HER") or (pronoun.upper() == "SHE") or (pronoun.upper() == "FEMALE") or (pronoun.upper() == "WOMAN") or (pronoun.upper() == "F") or (pronoun.upper() == "S")):
                role = r_her
            if ((pronoun.upper() == "THEM") or (pronoun.upper() == "THEY") or (pronoun.upper() == "IT") or (pronoun.upper() == "OTHER") or (pronoun.upper() == "T")):
                role = r_they

            #eprint("pronoun role: " + role.name);
            try:
                if role in message.author.roles:
                    await client.send_message(message.author, "You already had the role " + role.name + ", so I'm toggling it off. ")
                    eprint(message.author.name + " has role " +
                           role.name + ", removing.")
                    await client.remove_roles(message.author, role)
                else:
                    if role not in message.author.roles:
                        await client.send_message(message.author, "You did not have the role " + role.name + ", so I'm adding it now for you!")
                        eprint(message.author.name +
                               " does not have role " + role.name + ", adding.")
                        await client.add_roles(message.author, role)
            except BaseException as e:
                await client.send_message(message.author, "Either you did not specify a pronoun, or I don't know what you mean by " + pronoun + ". Sorry! If you think this is an error, please report it. ")
            await client.delete_message(message)
            return

        if message.content.startswith('!help'):
            await client.send_message(message.author, helpstr)
            await client.delete_message(message)
        if message.content.startswith('!verify'):
            if (modrole[message.server] in message.author.roles):
                verified = discord.utils.get(
                    lwu_server.roles, id='275764022547316736')
                for member in message.mentions:
                    # eprint(member.name)
                    # for role in member.roles:
                        # eprint(member.name)
                        # eprint(role.name)
                    if verified not in member.roles:
                        await client.add_roles(member, verified)
                        await client.send_message(message.channel, "Verified user " + member.name)
                    else:
                        await client.send_message(message.channel, "User is already verified: " + member.name)
            await client.send_message(workingChan, "Please welcome new user " + member.mention + " to the server!")
            await client.delete_message(message)
            return

        if message.content.startswith('!frugnuke '):
            if (modrole[message.server] in message.author.roles):
                msg = message.content[10:]
                print("Getting logs ")
                logs = await client.logs_from(message.channel, int(msg))

                print("Itterating  logs ")
                for logmessage in logs:
                         # python will convert \n to os.linesep
                    # await client.send_message(gio, message.author.name)

                    try:
                        print("Targetting " + logmessage.author.name)
                        await client.change_nickname(logmessage.author, "frug")
                    except BaseException as e:
                        print("error")

                await client.delete_message(message)
            return

    if message.server == None:  # Private Message
        with open(logpath(message), 'a+') as file:
            file.write("[" + message.author.name +"]: " + message.clean_content + "\n")

        if message.content.startswith('!emoji'):
            for s in client.get_all_emojis():
                print(s.name + ", " + s.id)

        if message.content.startswith('!help'):
            await client.send_message(message.author, helpstr)

        if message.author == gio:

            if message.content.startswith('!mention'):
                print(message.author.mention)
            if message.content.startswith('!hardreboot'):
                await client.send_message(message.author, "Here goes!")
                await client.send_message(message.author, os.system("sudo reboot"))
                return
            if message.content.startswith('!restart') or message.content.startswith('!reload'):
                await client.change_presence(game=discord.Game(name="swords", type=1))
                await client.delete_message(message)
                os.system("killall python3")
                return
            if message.content.startswith('!eval'):
                msg = message.content[6:]
                try:
                    eval(msg)
                except BaseException as e:
                    await client.send_message(message.author, str(e))

            elif message.content.startswith('!syseval'):
                msg = message.content[9:]
                try:
                    os.system(msg)
                except BaseException as e:
                    await client.send_message(message.author, str(e))
            elif message.content.startswith('!say'):
                msg = message.content[5:]
                print(type(msg))
                await client.send_message(workingChan, msg)

            elif message.content.startswith('!avatar'):
                msg = message.content[8:]
                fp = open(msg, 'rb')
                filestream = fp.read()
                await client.edit_profile(avatar=filestream)
                fp.close()

            elif message.content.startswith('!nick'):
                nickname = message.content[6:]
                await client.change_nickname(rubybot_member, nickname)

            elif message.content.startswith('!smol'):
                print("sending one smol")
                await client.send_message(workingChan, "<" + emotes[lwu_server] + ">")

                # await client.send_message(workingChan, "<:smolrubes:243554386549276672>")

            # elif message.content.startswith('!fakeupdate'):
                #lastPostID = '1'

            # elif message.content.startswith('!updebug'):
                # r = urllib.request.urlopen(feedurl).read()
                # r = r.decode()
                # #re.search('article', r)
                # mostRecentID = re.search('article.* data-post-id="(.*)"', r).group(1)
                # await client.send_message(message.author, "```" + str(lastPostID) + "/" + str(mostRecentID) + "```")

            elif message.content.startswith('!peribot'):
                await alias_peribot()
            elif message.content.startswith('!rubybot'):
                await alias_rubybot()
            elif message.content.startswith('!sapphire'):
                await alias_sapphy()

            elif message.content.startswith('!chan'):
                msg = message.content[6:]
                workingChan = client.get_channel(msg)
                await client.send_message(message.author, workingChan.name)

            elif message.content.startswith('!log'):
                logno = int(message.content[5:])
                for channel in lwu_server.channels:
                    logs = await client.logs_from(channel, logno)
                    f = open('/media/bluebook/logs/' +
                             channel.name + '.log', 'w')
                    await client.send_message(message.author, "Logged " + channel.name)
                    for message in logs:
                        f.write(str(message.timestamp) + " " + message.author.name + ": " + message.content +
                                ' ' + json.dumps(message.attachments) + '\n')  # python will convert \n to os.linesep
                    f.close()
                print("done")

    #toc = time.clock()
    #print("Message processing time: " + str(toc - tic))


eprint("Parsed Code")

filehandler = open("token", 'rb')
token = pickle.load(filehandler)
filehandler.close()

while True:
    try:
        eprint("Running client")
        client.run(token)
        eprint("Successful completion?")
    except RuntimeError:
        eprint("Major fault - Runtime error")
        traceback.print_exc(file=sys.stdout)
        os.system("killall python3")
    except Exception:
        eprint("Major fault")
        traceback.print_exc(file=sys.stdout)
        #os.system("killall python3")
