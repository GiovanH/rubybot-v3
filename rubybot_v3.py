#from __future__ import print_function
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

rbot.permissions = {
    '232218346999775232': {  # LWU
        '388738370676719616': 1,  # "mod"
        '388739472730357773': 1, #"tadpole"
        '233020731779317761': 2  #Bossman
    },
    '290270624558088192':{ #Minda
        '298390405169283072': 1,
        '290270933304999936': 2
    },
    '358806463139020810':{ #MU
        '358829062233260032': 1
    },
    '245789672842723329':{ #Tabuu
        '258320487698923520': 1,
        '245790823499825153': 2
    }
}
#ENUMS

emotes = {}
async def emote(server, match, braces):
    default = "smolrubes"
    fallback = None
    m = None
    try:
        m = emotes[match][server.id]
    except KeyError as exception:
        for e in server.emojis:
            if default == e.name:
                fallback = e
            if match == e.name:
                m = e
        if m: #matched perfectly
            pass
        elif fallback:
            m = fallback
        else:
            with open("asset/" + default + ".png", 'rb') as fp:
                bytes = fp.read()
                print("I'm being forced to add an emoji to " + server.name)
                m = await client.create_custom_emoji(server=server, name=default, image=bytes)
        if emotes.get(match) == None: emotes[match] = {}
        emotes[match][server.id] = m
    s = ":" + m.name + ":" + m.id
    if braces:
        return "<" + s + ">"
    else:
        return s

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

    """Called when discord logs in. Initializes things. """

    server_mu = rbot.Server(client, 358806463139020810)  # Moderation United
    server_lwu = rbot.Server(client, 232218346999775232)  # lwu
    server_tabuu = rbot.Server(client, 245789672842723329)  # TABUU
    server_minda = rbot.Server(client, 290270624558088192)  # Minda

    for c in client.servers:
        allowed = False
        for s in rbot.servers:
            if s == c.id: allowed = True
        if not allowed:
            await client.send_message(s.owner, "I am not authorized to be in " + s.name + "! It's ID, " + s.id + ", is not in my list. Leaving. ")
            await client.leave_server(s)

    print('Logged in as ' + client.user.name + " @<" + client.user.id + ">")

    loop = asyncio.get_event_loop()
    print('Creating update loop for LWU')
    loop.create_task(background_check_feed(loop, 'http://loreweaver-universe.tumblr.com/',
                                           client.get_channel('388730628176084992'), client.get_channel('388802759077658665'), 90))
    print('Creating update loop for Minda')
    loop.create_task(background_check_feed(loop, 'http://mindareadsoots.tumblr.com/',
                                           client.get_channel('290270624558088192'), client.get_channel('298828535894769665'), 90))

    loop.create_task(fear_of_death(550))

    await loadfrogs()
    try:
        with open("last_trace.log", "r") as tracefile:
            await client.send_message(gio, "I just came online. Last error: \n" + tracefile.read())
        with open("git.log", "r") as _file:
            await client.send_message(gio, "Latest git revision: \n" + _file.read())
        with open("last_trace.log", 'w', newline='\r\n') as tracefile2:
            tracefile2.write(
                "Nothing known! No exception written to file!")
            tracefile2.flush()
    except:
        pass

    cmd_test = rbot.Command('test', (lambda message:
        client.send_message(gio, "Message")
    ),
    'Test command',  # helpstr
    3)  # Permission Level

    def cmd_error_func(message):
        m = [1]
        print(m[3])
    cmd_error = rbot.Command('raise', cmd_error_func, 'Throws an error', 0)

    async def cmd_vote_func(message):
        splittoken = '; '
        reaction_dict = random.choice(
            ['🇦🇧🇨🇩🇪🇫🇬🇭', '❤💛💚💙💜🖤💔', '🐶🐰🐍🐘🐭🐸', '🍅🍑🍒🍌🍉🍆🍓🍇']
        )
        options = ' '.join(message.content.split()[1:]).split(splittoken)  # Remove first word, Create list
        pollmsg = await client.send_message(message.channel, "Loading...")
        polltext = message.author.name + " has called a vote:"
        i = 0
        for o in options:
            polltext = polltext + "\n" + reaction_dict[i] + ": " + o
            print(reaction_dict[i])
            await client.add_reaction(pollmsg, reaction_dict[i])
            i = i + 1
        await client.edit_message(pollmsg, new_content=polltext)
    cmd_vote = rbot.Command('callvote', cmd_vote_func,
    'List options seperated by \'; \' to prompt a vote. ',  # helpstr
    0)  # Permission Level

    async def cmd_listroles_func(message):
        m = ""
        for role in message.server.roles:
            m += str(role.name) + ": " + str(role.id) + "\n"
        await client.send_message(message.author, m)
    cmd_listroles = rbot.Command('listroles', cmd_listroles_func,
    'Messages you with all roles from a server',  # helpstr
    2)  # Permission Level

    async def cmd_wwheek_func(message):
        print('wwheekin')
        r = urllib.request.urlopen("https://wwheekadoodle.tumblr.com/rss").read()
        r = r.decode()
        img = random.choice(re.compile('img src="([^"]+)').findall(r))
        await client.send_message(message.channel, img)
    cmd_wwheek = rbot.Command('wwheek', cmd_wwheek_func,
    'wwheeks a wwheek',  # helpstr
    0)  # Permission Level

    async def cmd_sayhere_func(message):
        text = " ".join(message.content.split()[1:])
        await client.delete_message(message)
        await client.send_message(message.channel, text)
    cmd_sayhere = rbot.Command('sayhere', cmd_sayhere_func,
    'Echos your message back where you post this command',  # helpstr
    3)  # Permission Level

    async def cmd_frog_func(message):
        await client.send_typing(message.channel)
        print(len(froggos))
        frogi = random.randint(1, len(froggos))
        froggo = froggos[frogi-1]
        await client.send_message(message.channel, "[" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": " + froggo)
        await client.delete_message(message)
        return
    cmd_frog = rbot.Command('frog', cmd_frog_func,
    'Gives a froggo',  # helpstr
    0)  # Permission Level
    cmd_contraband = rbot.Command('contraband', cmd_frog_func,
    'Alias for frog',  # helpstr
    0)  # Permission Level

    async def cmd_addfrog_func(message):
        msg = " ".join(message.content.split()[1:])
        frogfile = 'frogs.frog'
        try:
            urllib.request.urlopen(msg).read()
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as e:
            await client.send_message(message.channel, "Check failed! Bad link? Details in log. Ignore this message if the link came from discord, or if the image shows up anyway.")
            traceback.print_exc(file=sys.stdout)
            # return
        #fh = open(frogfile, 'a')
        #fh.write(msg + "\n")
        froggos.extend(msg)
        #uniqlines = set(open(frogfile).readlines())
        uniqlines = open(frogfile).readlines()
        uniqlines.insert(0, msg + "\n")
        open(frogfile, 'w').writelines(set(uniqlines))
        await loadfrogs()
        await client.send_message(message.channel, "Added frog.")
    cmd_addfrog = rbot.Command('addfrog', cmd_addfrog_func,
    'Adds a frog to the frog dictionary',  # helpstr
    2)  # Permission Level

    async def cmd_removefrog_func(message):
        msg = " ".join(message.content.split()[1:])
        frogfile = 'frogs.frog'
        try:
            urllib.request.urlopen(msg).read()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            await client.send_message(message.channel, "Check failed! Bad link? Details in log. Ignore this message if the link came from discord, or if the image shows up anyway.")
            traceback.print_exc(file=sys.stdout)
            # return
        #fh = open(frogfile, 'a')
        #fh.write(msg + "\n")
        uniqlines = open(frogfile).readlines()
        #print(uniqlines)[5]
        print(msg)
        try:
            uniqlines.remove(msg + "\n")
            froggos.remove(msg)
            #await client.send_message(message.channel, "Removing that frog.")
        except:
            print(uniqlines)
            print(msg)
            traceback.print_exc(file=sys.stdout)
            await client.send_message(message.channel, "There may have been an error.")

        open(frogfile, 'w').writelines(set(uniqlines))
        await loadfrogs()
        await client.send_message(message.channel, "Removed frog.")
    cmd_removefrog = rbot.Command('removefrog', cmd_removefrog_func,
    'Removes a frog from the frog dictionary',  # helpstr
    2)  # Permission Level

    async def cmd_listemotes_func(message):
        m = ""
        for s in message.server.emojis:
            m += s.name + "\t" + s.id + "\t" + s.url + "\n"
        await send_message_smart(message.author, m)
    cmd_listemotes = rbot.Command('listemotes', (cmd_listemotes_func),
    'Messages you the server\'s emotes',  # helpstr
    1)  # Permission Level

    async def cmd_pm_func(message):
        for m in message.mentions:
            target = m
            if target == None:
                await client.send_message(message.channel, "No such person")
                break
            content = " ".join(message.content.split()[1:])
            await client.send_message(target, content)
        await client.delete_message(message)
    cmd_ = rbot.Command('pm', cmd_pm_func,
    'Sends a PM to one person mentioned',  # helpstr
    3)  # Permission Level

    async def cmd_restart_func(message):
        await client.change_presence(game=discord.Game(name="swords", type=1))
        try:
            await client.add_reaction(message, await emote(message.server, 'smolrubes',False))
        except:
            pass
        eprint("Restarting rubybot at request of " +
               message.author.name)
        with open("last_trace.log", "w") as f:
            f.write("Restarted at request of " +
                    message.author.name)
            f.flush()
        sys.exit(0)
    cmd_restart = rbot.Command('restart', cmd_restart_func,
    'Restarts rubybot',  # helpstr
    2)  # Permission Level
    cmd_reload = rbot.Command('reload', cmd_restart_func,
    'Alias of restart',  # helpstr
    2)

    async def cmd_permissions_func(message):
        p = rbot.permissionLevel(message.author, message.server)
        pss = ['Everyone', 'Moderator', 'Admin', 'Super Admin']
        ps = pss[p]
        await client.send_message(message.channel, message.author.name + ", your permission level in this server is " + str(p) + " (" + ps + ")")
    cmd_permissions = rbot.Command('permissions', cmd_permissions_func,
    'Tells you your permissions level in context',  # helpstr
    0)  # Permission Level

    async def cmd_roll_func(message):
        dice = " ".join(message.content.split()[1:])
        bonus = 0
        drops = 0
        try:
            if "+" in dice:
                dice, bonus = map(str, dice.split(' +'))
            if "droplowest" in dice:
                dice, drops = map(str, dice.split(' droplowest '))
            elif "-" in dice:
                dice, drops = map(str, dice.split(' -'))
            rolls, limit = map(int, dice.split('d'))
        except Exception:
            await client.send_message(message.channel, "I don't understand that dice notation! The format is NdN +N")
            return
        bonus = int(bonus)
        drops = int(drops)
        if rolls + limit > 200:
            await client.send_message(message.channel, "Hey, I'm really sorry " + message.author.mention + ", but I can't do that in my head. :c")
            return
        result = rollplain(rolls, limit)
        resultsstr = ', '.join(str(result[r]) for r in range(rolls))
        if rolls > 1:
            total = totalDelimitedList(result, drops)
            await client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + "\nTotal: " + str(total) + "+ " + str(bonus) + " = " + str(total + bonus))
        else:
            await client.send_message(message.channel, message.author.mention + "'s roll:\n" + resultsstr + " + " + str(bonus) + " = " + str(result[0] + bonus))
        if ((rolls == 4) and (limit == 20)) or (rolls == 69) or (limit == 69):
            await client.send_message(message.channel, "you meme-loving degenerates.")
    cmd_roll = rbot.Command('roll', cmd_roll_func,
    'Rolls fancy dice',  # helpstr
    0)  # Permission Level

    async def cmd_reteam_func(message):

        taboo_teams = []
        taboo_server = rbot.servers['245789672842723329'].server
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='246194907302199296'))  # add team
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755561359081473'))  # red team
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755634402623499'))  # rocket
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755659996397568'))  # blue
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388806422370058249'))  # illum
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388806560006144012'))  # choice
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388807162001883149'))  # sports
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
    cmd_reteam = rbot.Command('reteam', cmd_reteam_func,
    'Re-teams a member on taboo',  # helpstr
    1)  # Permission Level

    async def cmd_smolmote_func(message): #TODO: Gotta localize the emotes
    msg = " ".join(message.content.split()[1:])
        try:
            chan = client.get_channel(msg[1])
            await client.send_message(chan, await emote(chan.server, 'smolrubes', True))
        except AttributeError:
            await client.send_message(message.author, "No such channel as " + msg[1])
    cmd_smolmote = rbot.Command('smol', cmd_smolmote_func,
    'Sends a smol to channel by ID',  # helpstr
    3)  # Permission Level

    async def cmd_nickname_func(message):
        nickname = " ".join(message.content.split()[1:])
        await client.change_nickname(rubybot_member, nickname)
    cmd_nickname = rbot.Command('nick', cmd_nickname_func,
    'Changes nickname',  # helpstr
    3)  # Permission Level

    async def cmd_avatar_func(message):
        msg = " ".join(message.content.split()[1:])
        fp = open(msg, 'rb')
        filestream = fp.read()
        await client.edit_profile(avatar=filestream)
        fp.close()
    cmd_avatar = rbot.Command('avatar', cmd_avatar_func,
    'Sets avatar',  # helpstr
    3)  # Permission Level

    async def cmd_sayat_func(message): #TODO: Gotta localize the emotes
        msg = message.content.split()
        try:
            await client.send_message(client.get_channel(msg[1]), " ".join(msg[2:]))
        except discord.errors.InvalidArgument:
            await client.send_message(message.author, "No such channel as " + msg[1])
    cmd_sayat = rbot.Command('say', cmd_sayat_func,
    'Says a message at a channel by ID',  # helpstr
    3)  # Permission Level

    async def cmd_hardreboot_func(message):
        await client.send_message(message.author, "Here goes!")
        await client.send_message(message.author, os.system("sudo reboot"))
    cmd_hardreboot = rbot.Command('hardreboot', cmd_hardreboot_func,
    'sudo reboot',  # helpstr
    3)  # Permission Level

    async def cmd_help_func(message):
        helpstr = message.author.name + "'s list of availible commands (in context):"
        if message.server:
            for command in rbot.servers[message.server.id].commands:
                if rbot.permissionLevel(message.author, message.server) >= command.permlevel:
                    helpstr += "\n!" + command.name + " : " + command.helpstr
            await send_message_smart(message.channel, helpstr)
        else:
            for command in rbot.direct_commands:
                if rbot.permissionLevel(message.author, message.server) >= command.permlevel:
                    helpstr += "\n!" + command.name + " : " + command.helpstr
            await send_message_smart(message.author, helpstr)
    cmd_help = rbot.Command('help', cmd_help_func,
    'List availible commands and their functions',  # helpstr
    0)  # Permission Level

    async def cmd_allhelp_func(message):
        helpstr = message.author.name + "'s list of availible commands (in context):"
        if message.server:
            for command in rbot.servers[message.server.id].commands:
                helpstr += "\n(" + str(command.permlevel) + ") !" + command.name + " : " + command.helpstr
            await client.send_message(message.channel, helpstr)
        else:
            for command in rbot.direct_commands:
                helpstr += "\n(" + str(command.permlevel) + ") !" + command.name + " : " + command.helpstr
            await client.send_message(message.author, helpstr)
    cmd_allhelp = rbot.Command('allhelp', cmd_allhelp_func,
    'List all commands and their permission level',  # helpstr
    1)  # Permission Level

    async def cmd_rules_func(message):
        with open("rules/" + message.server.id, 'r') as rulefile:
            await client.send_message(message.channel, rulefile.read())
    cmd_rules = rbot.Command('rules', cmd_rules_func,
    'Lists the server\'s rules',  # helpstr
    0)  # Permission Level

    async def cmd_setrules_func(message):
        with open("rules/" + message.server.id, 'w') as rulefile:
            rulefile.write(" ".join(message.content.split()[1:]))
            rulefile.flush()
            await client.send_message(message.channel, "Rules updated. Use the rules command to test.")
    cmd_setrules = rbot.Command('setrules', cmd_setrules_func,
    'Modifies the server\'s rules',  # helpstr
    2)  # Permission Level

    async def cmd_pins_func(message):
        await client.send_typing(message.channel)
        pins = await client.logs_from(client.get_channel('278819870106451969'), limit=400)
        pinmsg = random.choice(list(pins))
        pinurl = pinmsg.content
        for a in pinmsg.attachments:
            pinurl += "\n" + a.get('url')
        await client.send_message(message.channel, "Pin from " + pinmsg.author.name + " from " + str(pinmsg.timestamp) + ": " + pinurl)
        await client.delete_message(message)
    cmd_pins = rbot.Command('pins', cmd_pins_func,
    'Posts a random pinned message',  # helpstr
    0)  # Permission Level

    async def cmd_bad_func(message):
        source = message.author
        for target in message.mentions:
            if target == None:
                await client.send_message(message.channel, "No such person")
                await client.delete_message(message)
                return
            if source == None:
                source = rubybot_member
            badr = discord.utils.get(
                server_lwu.server.roles, id='388739766025191435')
            verified = discord.utils.get(
                server_lwu.server.roles, id='388737413213716481')
            i = 1
            while (badr not in target.roles):
                i = i + 1
                await client.add_roles(target, badr)
            while (verified in target.roles):
                i = i + 1
                await client.remove_roles(target, verified)
            await client.send_message(message.channel, target.name + " has been badded to the pit by " + source.name + ".")
            #await client.send_message(modchat, "Log: " + target.name + " has been badded to the pit by " + source.name)
        await client.delete_message(message)
    cmd_bad = rbot.Command('bad', cmd_bad_func,
    'Bad them to the pit!',  # helpstr
    1)  # Permission Level

    async def cmd_unbad_func(message):
        source = message.author
        for target in message.mentions:
            if target == None:
                await client.send_message(message.channel, "No such person")
                await client.delete_message(message)
                return
            badr = discord.utils.get(
                server_lwu.server.roles, id='388739766025191435')
            verified = discord.utils.get(
                server_lwu.server.roles, id='388737413213716481')
            # await client.remove_roles(target, badr)
            i = 1
            while (badr in target.roles):
                i = i + 1
                await client.remove_roles(target, badr)
            while (verified not in target.roles):
                i = i + 1
                await client.add_roles(target, verified)
            # await client.send_message(workingChan, target.name + " has been unbadded by " + source.name)
            await client.send_message(message.channel, "Log: " + target.name + " has been unbadded by " + source.name + ".")
        await client.delete_message(message)
    cmd_unbad = rbot.Command('unbad', cmd_unbad_func,
    'unBad them from the pit!',  # helpstr
    1)  # Permission Level

    async def cmd_pronoun_func(message):
        pronoun = " ".join(message.content.split()[1:])
        r_him = discord.utils.get(message.server.roles, id='388740839943438336')
        r_her = discord.utils.get(message.server.roles, id='388740921975373835')
        r_they = discord.utils.get(message.server.roles, id='388740870641287169')

        if ((pronoun.upper() == "HIM") or (pronoun.upper() == "HE") or (pronoun.upper() == "MALE") or (pronoun.upper() == "MAN") or (pronoun.upper() == "M") or (pronoun.upper() == "H")):
            role = r_him
        if ((pronoun.upper() == "HER") or (pronoun.upper() == "SHE") or (pronoun.upper() == "FEMALE") or (pronoun.upper() == "WOMAN") or (pronoun.upper() == "F") or (pronoun.upper() == "S")):
            role = r_her
        if ((pronoun.upper() == "THEM") or (pronoun.upper() == "THEY") or (pronoun.upper() == "IT") or (pronoun.upper() == "OTHER") or (pronoun.upper() == "T")):
            role = r_they
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
    cmd_pronoun = rbot.Command('pronoun', cmd_pronoun_func,
    'Gives you a pronoun role so people know what to call you. Specify a pronoun after the command',  # helpstr
    0)  # Permission Level

    async def cmd_verify_func(message):
        workingChan = client.get_channel('388730628176084992')
        verified = discord.utils.get(message.server.roles, id='388737413213716481')
        for member in message.mentions:
            if verified not in member.roles:
                await client.add_roles(member, verified)
                await client.send_message(message.channel, "Verified user " + member.name)
            else:
                await client.send_message(message.channel, "User is already verified: " + member.name)
        await client.send_message(workingChan, "Please welcome new user " + member.mention + " to the server!")
        await client.delete_message(message)
    cmd_verify = rbot.Command('verify', cmd_verify_func,
    'Verifies a user',  # helpstr
    1)  # Permission Level

    async def cmd_fund_func(message):
        # await client.send_message(message.channel, "Keep me from dying a painful death! https://www.patreon.com/giovan")
        await client.send_message(message.channel,embed=discord.Embed(title="Keep me from dying a horrible, painful death!",url="https://www.patreon.com/giovan").set_author(name="Giovan").set_thumbnail(url="https://cdn.discordapp.com/emojis/361958691244867584.png"))
    cmd_fund = rbot.Command('fund', cmd_fund_func,
    'Gives information about patreon',  # helpstr
    0)  # Permission Level
    cmd_patreon = rbot.Command('patreon', cmd_fund_func,
    'Alias for fund',  # helpstr
    0)  # Permission Level
    
    async def cmd_frig_func(message):
        # await client.send_message(message.channel, "Keep me from dying a painful death! https://www.patreon.com/giovan")
        await client.send_message(message.channel,"http://www.qwantz.com/comics/comic2-1348.png")
    cmd_frig = rbot.Command('frig', cmd_frig_func,
    'like, frig, man!',  # helpstr
    0)  # Permission Level
    
    # async def cmd__func(message):
    # cmd_ = rbot.Command('', cmd__func,
    # '',  # helpstr
    # 0)  # Permission Level
    cmdlist_base =    [
        cmd_frig,
        cmd_fund,
        cmd_patreon,
        cmd_vote,
        cmd_listroles,
        cmd_sayhere,
        cmd_frog,
        cmd_removefrog,
        cmd_listemotes,
        cmd_restart,
        cmd_reload,
        cmd_permissions,
        cmd_roll,
        cmd_nickname,
        cmd_avatar,
        cmd_help,
        cmd_allhelp,
        cmd_rules,
        cmd_setrules
    ]
    cmdlist_util =    [
        cmd_test,
        cmd_error,
        cmd_sayat,
        cmd_smolmote,
        cmd_hardreboot
    ]
    cmdlist_lwu_extras =    [
        cmd_addfrog,
        cmd_pins,
        cmd_bad,
        cmd_unbad,
        cmd_pronoun,
        cmd_verify,
        cmd_wwheek
    ]
    server_lwu.add_cmds(cmdlist_base + cmdlist_lwu_extras) #Temporary: All commands to LWU

    server_minda.add_cmd(cmd_smolmote) #Temporary: All commands to LWU
    server_minda.add_cmds(cmdlist_base) #Temporary: All commands to LWU
    server_minda.add_cmd(cmd_contraband)

    server_tabuu.add_cmds(cmdlist_base) #Temporary: All commands to LWU
    server_tabuu.add_cmd(cmd_wwheek) #Temporary: All commands to LWU

    server_mu.add_cmds(cmdlist_base) #Temporary: All commands to LWU
    server_mu.remove_cmds([cmd_frog])
    server_tabuu.add_cmd(cmd_reteam)

    rbot.direct_commands = list(cmdlist_base + cmdlist_util) #Temporary: All commands to PM
    #import pdb; pdb.set_trace()

@client.event
async def on_message_edit(before, after):
    message = after
    fmt = '**{0.author}** edited their message from: |{1.content}| to |{0.content}|\n'
    if message.server:
        with open(logpath(message), 'a+') as file:
            file.write(fmt.format(after, before))
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
    else:
        with open(logpath(message), 'a+') as file:
            file.write(fmt.format(after, before))
            file.write(message.author.name + ": " +
                       message.clean_content + "\n")

@client.event
async def on_message_delete(message):
    if message.server:
        fmt = '{0.author.name} has deleted the message: |{0.content}|\n'
        with open(logpath(message), 'a+') as file:
            file.write(fmt.format(message))
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
    else:
        fmt = '{0.author.name} has deleted the message: |{0.content}|\n'
        with open(logpath(message), 'a+') as file:
            file.write(fmt.format(message))
            file.write(message.author.name + ": " +
                       message.clean_content + "\n")

@client.event
async def on_member_join(member):
    if rbot.servers.get('245789672842723329') and member.server is rbot.servers['245789672842723329'].server:
        eprint("setting team in taboo")
        target = member

        taboo_teams = []
        taboo_server = rbot.servers['245789672842723329'].server
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='246194907302199296'))  # add team
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755561359081473'))  # red team
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755634402623499'))  # rocket
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388755659996397568'))  # blue
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388806422370058249'))  # illum
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388806560006144012'))  # choice
        taboo_teams.append(discord.utils.get(taboo_server.roles,
                                          id='388807162001883149'))  # sports
        newteam = random.choice(taboo_teams)
        await client.add_roles(target, newteam)
        for role in taboo_teams:
            # await client.send_message(message.channel, "Checking role " + role.name)
            if (role in target.roles) and (role is not newteam):
                # await client.send_message(message.channel, "Removing role " + role.name)
                await client.remove_roles(target, role)
        await client.send_message(member.server.default_channel, "Please welcome " + target.mention + " to " + newteam.name)


async def fear_of_death(freq):
    #global timezone
    if (not client.is_logged_in) or (client.is_closed):
        print("Oh no, the client closed???")
        print("Client error. Status: \n\tLogged in: " + str(client.is_logged_in) + "\n\tClosed: " + str(client.is_closed))
        sys.exit()


async def background_check_feed(asyncioloop, feedurl, workingChan, rubychan, freq):
    #global timezone
    import time
    mostRecentID = '1'
    lastPostID = '0'
    update_delay = 0
    time_lastupdate = time.time()
    # Basically run forever
    while not client.is_closed:
        try:
            r = urllib.request.urlopen(feedurl).read()
            r = r.decode()
            mostRecentID = re.search(
                'article.* data-post-id="(.*)"', r).group(1)
            if mostRecentID != lastPostID:
                if '0' != lastPostID:
                    print(feedurl + " change: " + lastPostID + " =/= " + mostRecentID)
                    print(feedurl + " update: " +
                          lastPostID + " -> " + mostRecentID)
                    print("Time since last update: " + str(time.time() - time_lastupdate) + " sec")
                    print("Delay at time of update: " + str(update_delay))
                    time_lastupdate = time.time()
                    update_delay = 0
                    await client.send_message(rubychan, "[[ " + "Update! " + feedurl + "post/" + mostRecentID + "/ ]]")
                    await client.send_message(workingChan, await emote(workingChan.server, 'smolrubes', True) + "[[ Update! ]]")
                elif update_delay < (10*60):
                    update_delay += 10
                lastPostID = mostRecentID
                print(lastPostID)
        except:
            eprint("error fetching status for " + feedurl)
            traceback.print_exc()
            traceback.print_exc(file=sys.stdout)
            # No matter what goes wrong, wait same time and try again
        finally:
            await asyncio.sleep(freq + update_delay)

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
    array2 = array2[number:]
    for i in array2:
        total += i
    return total

@client.event
async def on_message(message):
    #tic = time.clock()
    # we do not want the bot to react to itself
    if message.author == client.user:
        return

    if message.server != None:  # Generic Server
        if "rubybot" in message.content.lower():
            #print("Debug: i've beem nentioned!")
            await client.add_reaction(message, await emote(message.server, 'smolrubes',False))
            #return

        if "boobybot" in message.content.lower():
            #print("Debug: i've beem nentioned!")
            await client.add_reaction(message, await emote(message.server, 'rubyblush', False))
            #return

        if "wwheek" in message.content.lower():
            #print("Debug: i've beem nentioned!")
            await client.add_reaction(message, '💚')
            #return


    if message.server:
        with open(logpath(message), 'a+') as file:
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
            if message.attachments:
                file.write("[" + message.channel.name + "] " +
                           message.author.name + ": " + str(message.attachments) + "\n")
        for command in rbot.servers[message.server.id].commands:
        #try:
            await command.run(message)
        # except NameError:
        #     await client.send_message(message.channel, "You lack permissions for that operation")

    else:
        with open(logpath(message), 'a+') as file:
            file.write("[" + message.author.name + "] " +
                       ": " + message.clean_content + "\n")
        for command in rbot.direct_commands:
            await command.run(message)

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
