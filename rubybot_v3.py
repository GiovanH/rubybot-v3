# !python3

import discord
import random
import traceback
import asyncio
import re
import pickle
import urllib.request
import os
import datetime
import sys
import rubybot_classes as rbot
import rubybot_util as rutil
import jfileutil
import pytumblr

MAX_UPDATE_DELAY = 15 * 60  # Fifteen minutes
LOADED = False

client = discord.Client()
rutil.client = client

# Load permissions file from json
rbot.permissions = jfileutil.load("permissions")
emotes = {}

###############################
# Make emote enumeration
###############################


# Returns the text representation of the requested emote, specific to the server
# @param server
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
        if m:  # matched perfectly
            pass
        elif fallback:
            m = fallback
        else:
            with open("asset/" + default + ".png", 'rb') as fp:
                bytes = fp.read()
                print("I'm being forced to add an emoji to " + server.name)
                m = await client.create_custom_emoji(server=server, name=default, image=bytes)
        if emotes.get(match) is None:
            emotes[match] = {}
        emotes[match][server.id] = m
    s = ":" + m.name + ":" + m.id
    if braces:
        return "<" + s + ">"
    else:
        return s

    ###############################
    # Make frog enumeration
    ###############################

froggos = []


async def loadfrogs():
    # frogurls = jfileutil.load("frogs")
    global froggos
    frogfetchers = [
        {
            "url": "http://allaboutfrogs.org/funstuff/randomfrog.html",
            "re": '"(http:\/\/www\.allaboutfrogs\.org\/funstuff\/random\/.*?)"'
        },
        {
            "url": "http://stickyfrogs.tumblr.com/tagged/frogfriends",
            "re": 'img src="(.*?)"'
        },
        {
            "url": "https://twitter.com/stickyfrogs/media",
            "re": 'img data-aria-label-part src="(.*?)"'
        },
        {
            "url": "https://twitter.com/Litoriacaeru/media",
            "re": 'img data-aria-label-part src="(.*?)"'
        }
    ]
    frogurls = []
    for method in frogfetchers:
        try:
            r = urllib.request.urlopen(method['url']).read()
            r = r.decode()
            frogurls.extend(re.compile(method['re']).findall(r))
        except:
            traceback.print_exc(file=sys.stdout)
            rutil.eprint("frog error, continuing")

    froggos = []
    for d in jfileutil.load("frogsmd5"):
        try:
            froggos.append(rbot.Frog(d))
        except:
            print("Could not add frog with data " + d)

    for url in frogurls:
        for frog in froggos:
            if frog.data['url'] == url:
                break
        else:
            try:
                froggos.append(rbot.Frog({'url': url}))
            except:
                print("Could not add frog with url " + url)
    save_frogs()

def save_frogs():
    global froggos
    froggos = sorted(list(set(froggos)))
    jfileutil.save([f.data for f in froggos], "frogsmd5")

# Initialization


@client.event
async def on_ready():

    ###############################
    # Initial Loading
    ###############################
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
            if s == c.id:
                allowed = True
        if not allowed:
            await client.send_message(s.owner, "I am not authorized to be in " + s.name + "! It's ID, " + s.id + ", is not in my list. Leaving. ")
            await client.leave_server(s)

    print('Logged in as ' + client.user.name + " @<" + client.user.id + ">")

    loop = asyncio.get_event_loop()
    print('Creating update loops')
    tumblr_polls = jfileutil.load("polls")

    for t in tumblr_polls:
        print('Creating update loop for ' + t['blogname'])
        loop.create_task(
            background_check_feed(
                loop,
                t['blogname'],
                client.get_channel(t['bigchannel']),
                client.get_channel(t['minichannel']),
                t['mindelay']
            )
        )

        # loop.create_task(background_check_feed(loop, 'http://loreweaver-universe.tumblr.com/',
        #                                        client.get_channel('388730628176084992'), client.get_channel('388802759077658665'), 45))
        # loop.create_task(background_check_feed(loop, 'http://mindareadsoots.tumblr.com/',
        #                                        client.get_channel('290270624558088192'), client.get_channel('298828535894769665'), 90))

    loop.create_task(fear_of_death(550))

    await loadfrogs()
    try:
        with open("last_trace.log", "r") as tracefile:
            await client.send_message(gio, "I just came online. Last error: \n" + tracefile.read())
        with open("git.log", "r") as _file:
            await rutil.send_message_smart(gio, "Latest git revision: \n" + _file.read())
        with open("last_trace.log", 'w', newline='\r\n') as tracefile2:
            tracefile2.write(
                "Nothing known! No exception written to file!")
            tracefile2.flush()
    except:
        traceback.print_exc(file=sys.stdout)
    global LOADED
    LOADED = True

    ###############################
    # Commands and command handling
    ###############################

    rbot.Command('test', (lambda message:
                          client.send_message(gio, "Message")
                          ),
                 'Test command',  # helpstr
                 3)  # Permission Level

    def cmd_error_func(message):
        m = [1]
        print(m[3])
    rbot.Command('error', cmd_error_func, 'Throws an error', 0)

    async def cmd_vote_func(message):
        splittoken = '; '
        reaction_dict = random.choice(
            ['🇦🇧🇨🇩🇪🇫🇬🇭', '❤💛💚💙💜🖤💔', '🐶🐰🐍🐘🐭🐸', '🍅🍑🍒🍌🍉🍆🍓🍇']
        )
        options = ' '.join(message.content.split()[1:]).split(
            splittoken)  # Remove first word, Create list
        pollmsg = await client.send_message(message.channel, "Loading...")
        polltext = message.author.name + " has called a vote:"
        i = 0
        for o in options:
            polltext = polltext + "\n" + reaction_dict[i] + ": " + o
            print(reaction_dict[i])
            await client.add_reaction(pollmsg, reaction_dict[i])
            i = i + 1
        await client.edit_message(pollmsg, new_content=polltext)
    rbot.Command('callvote', cmd_vote_func,
                 'List options seperated by \'; \' to prompt a vote. ',   # helpstr
                 0)  # Permission Level

    async def cmd_listroles_func(message):
        m = ""
        for role in message.server.roles:
            m += str(role.name) + ": " + str(role.id) + "\n"
        await client.send_message(message.author, m)
    rbot.Command('listroles', cmd_listroles_func,
                 'Messages you with all roles from a server',  # helpstr
                 2)  # Permission Level

    async def cmd_wwheek_func(message):
        print('wwheekin')
        r = urllib.request.urlopen(
            "https://wwheekadoodle.tumblr.com/rss").read()
        r = r.decode()
        img = random.choice(re.compile('img src="([^"]+)').findall(r))
        await client.send_message(message.channel, img)
    rbot.Command('wwheek', cmd_wwheek_func,
                 "Gets a doodle from wwheek's tumblr",  # helpstr
                 0)  # Permission Level

    async def cmd_sayhere_func(message):
        text = " ".join(message.content.split()[1:])
        await client.delete_message(message)
        await client.send_message(message.channel, text)
    rbot.Command('sayhere', cmd_sayhere_func,
                 'Echos your message back where you post this command',  # helpstr
                 3)  # Permission Level

    async def cmd_frog_func(message):
        await client.send_typing(message.channel)
        print(len(froggos))
        frogi = random.randint(1, len(froggos))
        froggo = froggos[frogi - 1]
        await client.send_message(message.channel, "[" + str(frogi) + "/" + str(len(froggos)) + "] Frog for " + message.author.name + ": " + froggo.data['url'])
        await client.delete_message(message)
        return
    rbot.Command('frog', cmd_frog_func,
                 'Gives a froggo',  # helpstr
                 0)  # Permission Level
    rbot.Command('contraband', cmd_frog_func,
                 'Alias for frog',  # helpstr
                 0)  # Permission Level

    async def cmd_addfrog_func(message):
        global froggos
        msg = " ".join(message.content.split()[1:])
        try:
            print(msg)
            froggos.append(rbot.Frog({'url': msg}))
            save_frogs()
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as e:
            await client.send_message(message.channel, "Adding frog failed. Details in log.")
            traceback.print_exc(file=sys.stdout)

        await loadfrogs()
        await client.send_message(message.channel, "Added frog.")
    rbot.Command('addfrog', cmd_addfrog_func,
                 'Adds a frog to the frog dictionary',  # helpstr
                 2)  # Permission Level

    async def cmd_removefrog_func(message):
        global froggos
        msg = " ".join(message.content.split()[1:])
        try:
            i = 0
            for frog in froggos:
                if frog.data['url'] == msg:
                    froggos.remove(frog)
                    i += 1
                save_frogs()
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            await client.send_message(message.channel, "Check failed! Bad link? Details in log. Ignore this message if the link came from discord, or if the image shows up anyway.")
            traceback.print_exc(file=sys.stdout)
            return
        await loadfrogs()
        await client.send_message(message.channel, "Removed " + str(i) + " occurances of frog.")
    rbot.Command('removefrog', cmd_removefrog_func,
                 'Removes a frog from the frog dictionary',  # helpstr
                 2)  # Permission Level

    async def cmd_listemotes_func(message):
        m = ""
        for s in message.server.emojis:
            m += s.name + "\t" + s.id + "\t" + s.url + "\n"
        await rutil.send_message_smart(message.author, m)
    rbot.Command('listemotes', (cmd_listemotes_func),
                 'Messages you the server\'s emotes',  # helpstr
                 1)  # Permission Level

    async def cmd_pm_func(message):
        for m in message.mentions:
            target = m
            if target is None:
                await client.send_message(message.channel, "No such person")
                break
            content = " ".join(message.content.split()[1:])
            await client.send_message(target, content)
        await client.delete_message(message)
    cmd_pm = rbot.Command('pm', cmd_pm_func,
                        'Sends a PM to one person mentioned',  # helpstr
                        3)  # Permission Level

    async def cmd_restart_func(message):
        await client.change_presence(game=discord.Game(name="swords", type=1))
        try:
            await client.add_reaction(message, await emote(message.server, 'smolrubes', False))
        except:
            pass
        rutil.eprint("Restarting rubybot at request of " +
                     message.author.name)
        with open("last_trace.log", "w") as f:
            f.write("Restarted at request of " +
                    message.author.name)
            f.flush()
        sys.exit(0)
    rbot.Command('restart', cmd_restart_func,
                 'Restarts rubybot',  # helpstr
                 2)  # Permission Level
    rbot.Command('reload', cmd_restart_func,
                 'Alias of restart',  # helpstr
                 2)

    async def cmd_permissions_func(message):
        p = rbot.permissionLevel(message.author, message.server)
        pss = ['Everyone', 'Moderator', 'Admin', 'Super Admin']
        ps = pss[p]
        await client.send_message(message.channel, message.author.name + ", your permission level in this server is " + str(p) + " (" + ps + ")")
    rbot.Command('permissions', cmd_permissions_func,
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
    rbot.Command('roll', cmd_roll_func,
                 'Rolls fancy dice',  # helpstr
                 0)  # Permission Level

    async def cmd_reteam_func(message):
        msg = " ".join(message.content.split()[1:])

        taboo_server = rbot.servers['245789672842723329'].server
        taboo_teams = [
            discord.utils.get(taboo_server.roles, id=teamid) 
            for teamid in jfileutil.load("altgen_teams")
        ]
        targets = message.mentions
        if msg.lower()  == "all":
            targets = message.server.members
        for target in targets:
            newteam = taboo_teams[int(target.id)%len(taboo_teams)]
            await client.add_roles(target, newteam)
            for role in taboo_teams:
                # await client.send_message(message.channel, "Checking role " + role.name)
                if (role in target.roles) and (role is not newteam):
                    # await client.send_message(message.channel, "Removing role " + role.name)
                    await client.remove_roles(target, role)
            if msg.lower()  != "all":
                await client.send_message(message.channel, "Please welcome " + target.mention + " to " + newteam.name)
        await client.delete_message(message)
    rbot.Command('reteam', cmd_reteam_func,
                 'Re-teams a member on taboo',  # helpstr
                 2)  # Permission Level

    async def cmd_smolmote_func(message):  # TODO: Gotta localize the emotes
        msg = message.content.split()
        try:
            chan = client.get_channel(msg[1])
            await client.send_message(chan, await emote(chan.server, 'smolrubes', True))
        except AttributeError:
            await client.send_message(message.author, "No such channel as " + msg[1])
    rbot.Command('smol', cmd_smolmote_func,
                 'Sends a smol to channel by ID',  # helpstr
                 3)  # Permission Level

    async def cmd_nickname_func(message):
        nickname = " ".join(message.content.split()[1:])
        await client.change_nickname(rubybot_member, nickname)
    rbot.Command('nick', cmd_nickname_func,
                 'Changes nickname',  # helpstr
                 3)  # Permission Level

    async def cmd_avatar_func(message):
        msg = " ".join(message.content.split()[1:])
        try:
            with open(msg, 'rb') as fp:
                await client.edit_profile(avatar=fp.read())
        except:
            await client.send_message(message.author, traceback.format_exc())
    rbot.Command('avatar', cmd_avatar_func,
                 'Sets avatar',  # helpstr
                 3)  # Permission Level

    async def cmd_sayat_func(message):  # TODO: Gotta localize the emotes
        msg = message.content.split()
        try:
            await client.send_message(client.get_channel(msg[1]), " ".join(msg[2:]))
        except discord.errors.InvalidArgument:
            await client.send_message(message.author, "No such channel as " + msg[1])
    rbot.Command('say', cmd_sayat_func,
                 'Says a message at a channel by ID',  # helpstr
                 3)  # Permission Level

    async def cmd_hardreboot_func(message):
        await client.send_message(message.author, "Here goes!")
        await client.send_message(message.author, os.system("sudo reboot"))
    rbot.Command('hardreboot', cmd_hardreboot_func,
                 'sudo reboot',  # helpstr
                 3)  # Permission Level

    async def cmd_help_func(message):
        helpstrs = []
        if message.server:
            for command in rbot.servers[message.server.id].commands:
                if rbot.permissionLevel(message.author, message.server) >= command.permlevel:
                    helpstrs += ["!**" + command.name +
                                 "** : " + command.helpstr]
            helpstrs = sorted(helpstrs)
            helpstrs.insert(0, message.author.name +
                            "'s list of availible commands (in context):")
            await rutil.send_message_smart(message.channel, "\n".join(helpstrs))
        else:
            for command in rbot.direct_commands:
                if rbot.permissionLevel(message.author, message.server) >= command.permlevel:
                    helpstrs += ["!**" + command.name +
                                 "** : " + command.helpstr]
            helpstrs = sorted(helpstrs)
            await rutil.send_message_smart(message.author, "\n".join(helpstrs))
    rbot.Command('help', cmd_help_func,
                 'List availible commands and their functions',  # helpstr
                 0)  # Permission Level

    async def cmd_allhelp_func(message):
        helpstrs = []
        if message.server:
            for command in rbot.servers[message.server.id].commands:
                helpstrs += ["(" + str(command.permlevel) + ") !" +
                             command.name + " : " + command.helpstr]
            helpstrs = sorted(helpstrs)
            helpstrs.insert(0, message.author.name +
                            "'s list of availible commands (in context):")
            await rutil.send_message_smart(message.channel, "\n".join(helpstrs))
        else:
            helpstr = ""
            for command in rbot.direct_commands:
                helpstr += ["(" + str(command.permlevel) + ") !" +
                            command.name + " : " + command.helpstr]
            await rutil.send_message_smart(message.author, helpstr)
    rbot.Command('allhelp', cmd_allhelp_func,
                 'List all commands and their permission level',  # helpstr
                 1)  # Permission Level

    async def cmd_rules_func(message):
        await rutil.send_message_smart(message.channel, jfileutil.load("rules_" + message.server.id))
    rbot.Command('rules', cmd_rules_func,
                 'Lists the server\'s rules',  # helpstr
                 0)  # Permission Level

    async def cmd_setrules_func(message):
        # with open("rules/" + message.server.id, 'w') as rulefile:
        jfileutil.save(" ".join(message.content.split(' ')
                                [1:]), "rules_" + message.server.id)
        await client.send_message(message.channel, "Rules updated. Use the rules command to test.")
    rbot.Command('setrules', cmd_setrules_func,
                 'Modifies the server\'s rules',  # helpstr
                 2)  # Permission Level

    async def cmd_pins_func(message):
        await client.send_typing(message.channel)
        pins = await list(client.logs_from(client.get_channel('278819870106451969'), limit=400))
        pinmsg = random.choice(list(pins))
        pinurl = pinmsg.content
        for a in pinmsg.attachments:
            pinurl += "\n" + a.get('url')
        await client.send_message(message.channel, "Pin from " + pinmsg.author.name + " from " + str(pinmsg.timestamp) + ": " + pinurl)
        await client.delete_message(message)
    rbot.Command('pins', cmd_pins_func,
                 'Posts a random pinned message',  # helpstr
                 0)  # Permission Level

    async def cmd_bad_func(message):
        source = message.author
        for target in message.mentions:
            if target is None:
                await client.send_message(message.channel, "No such person")
                await client.delete_message(message)
                return
            if source is None:
                source = message.server.Client
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
            # await client.send_message(modchat, "Log: " + target.name + " has been badded to the pit by " + source.name)
        await client.delete_message(message)
    rbot.Command('bad', cmd_bad_func,
                 'Bad them to the pit!',  # helpstr
                 1)  # Permission Level

    async def cmd_unbad_func(message):
        source = message.author
        for target in message.mentions:
            if target is None:
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
    rbot.Command('unbad', cmd_unbad_func,
                 'unBad them from the pit!',  # helpstr
                 1)  # Permission Level

    async def cmd_pronoun_func(message):
        pronoun = " ".join(message.content.split()[1:])
        r_him = discord.utils.get(
            message.server.roles, id='388740839943438336')
        r_her = discord.utils.get(
            message.server.roles, id='388740921975373835')
        r_they = discord.utils.get(
            message.server.roles, id='388740870641287169')

        if ((pronoun.upper() == "HIM") or (pronoun.upper() == "HE") or (pronoun.upper() == "MALE") or (pronoun.upper() == "MAN") or (pronoun.upper() == "M") or (pronoun.upper() == "H")):
            role = r_him
        if ((pronoun.upper() == "HER") or (pronoun.upper() == "SHE") or (pronoun.upper() == "FEMALE") or (pronoun.upper() == "WOMAN") or (pronoun.upper() == "F") or (pronoun.upper() == "S")):
            role = r_her
        if ((pronoun.upper() == "THEM") or (pronoun.upper() == "THEY") or (pronoun.upper() == "IT") or (pronoun.upper() == "OTHER") or (pronoun.upper() == "T")):
            role = r_they
        try:
            if role in message.author.roles:
                await client.send_message(message.author, "You already had the role " + role.name + ", so I'm toggling it off. ")
                rutil.eprint(message.author.name + " has role " +
                             role.name + ", removing.")
                await client.remove_roles(message.author, role)
            else:
                if role not in message.author.roles:
                    await client.send_message(message.author, "You did not have the role " + role.name + ", so I'm adding it now for you!")
                    rutil.eprint(message.author.name +
                                 " does not have role " + role.name + ", adding.")
                    await client.add_roles(message.author, role)
        except BaseException as e:
            await client.send_message(message.author, "Either you did not specify a pronoun, or I don't know what you mean by " + pronoun + ". Sorry! If you think this is an error, please report it. ")
        await client.delete_message(message)
    rbot.Command('pronoun', cmd_pronoun_func,
                 'Gives you a pronoun role so people know what to call you. Specify a pronoun after the command',  # helpstr
                 0)  # Permission Level

    async def cmd_verify_func(message):
        workingChan = client.get_channel('388730628176084992')
        verified = discord.utils.get(
            message.server.roles, id='388737413213716481')
        for member in message.mentions:
            if verified not in member.roles:
                await client.add_roles(member, verified)
                await client.send_message(message.channel, "Verified user " + member.name)
            else:
                await client.send_message(message.channel, "User is already verified: " + member.name)
        await client.send_message(workingChan, "Please welcome new user " + member.mention + " to the server!")
        await client.delete_message(message)
    rbot.Command('verify', cmd_verify_func,
                 'Verifies a user',  # helpstr
                 1)  # Permission Level

    async def cmd_fund_func(message):
        await client.send_message(message.channel, embed=discord.Embed(title="Keep me alive and keep Gio healthy!", url="https://www.patreon.com/giovan").set_author(name="Giovan").set_thumbnail(url="https://cdn.discordapp.com/emojis/361958691244867584.png"))
    rbot.Command('fund', cmd_fund_func,
                 'Gives information about patreon',  # helpstr
                 0)  # Permission Level
    rbot.Command('patreon', cmd_fund_func,
                 'Alias for fund',  # helpstr
                 0)  # Permission Level

    async def cmd_frig_func(message):
        await client.send_message(message.channel, "http://www.qwantz.com/comics/comic2-1348.png")
    rbot.Command('frig', cmd_frig_func,
                 'like, frig, man!',  # helpstr
                 0)  # Permission Level

    # async def cmd__func(message):
    # cmd_ = rbot.Command('', cmd__func,
    # '',  # helpstr
    # 0)  # Permission Level
    cmdlist_base = [
        rbot.commands['frig'],
        rbot.commands['fund'],
        rbot.commands['patreon'],
        rbot.commands['callvote'],
        rbot.commands['listroles'],
        rbot.commands['sayhere'],
        rbot.commands['frog'],
        rbot.commands['removefrog'],
        rbot.commands['listemotes'],
        rbot.commands['restart'],
        rbot.commands['reload'],
        rbot.commands['permissions'],
        rbot.commands['roll'],
        rbot.commands['nick'],
        rbot.commands['avatar'],
        rbot.commands['help'],
        rbot.commands['allhelp'],
        rbot.commands['rules'],
        rbot.commands['setrules']
    ]
    cmdlist_util = [
        rbot.commands['test'],
        rbot.commands['error'],
        rbot.commands['say'],
        rbot.commands['smol'],
        rbot.commands['hardreboot']
    ]
    cmdlist_lwu_extras = [
        rbot.commands['addfrog'],
        rbot.commands['pins'],
        rbot.commands['bad'],
        rbot.commands['unbad'],
        rbot.commands['pronoun'],
        rbot.commands['verify'],
        rbot.commands['wwheek']
    ]
    # Temporary: All commands to LWU
    server_lwu.add_cmds(cmdlist_base + cmdlist_lwu_extras)

    # Temporary: All commands to LWU
    server_minda.add_cmd(rbot.commands['smol'])
    server_minda.add_cmds(cmdlist_base)  # Temporary: All commands to LWU
    server_minda.add_cmd(rbot.commands['contraband'])

    server_tabuu.add_cmds(cmdlist_base)  # Temporary: All commands to LWU
    # Temporary: All commands to LWU
    server_tabuu.add_cmd(rbot.commands['wwheek'])

    server_mu.add_cmds(cmdlist_base)  # Temporary: All commands to LWU
    server_mu.remove_cmds([rbot.commands['frog']])
    server_tabuu.add_cmd(rbot.commands['reteam'])

    # Temporary: All commands to PM
    rbot.direct_commands = list(cmdlist_base + cmdlist_util)
    # import pdb; pdb.set_trace()


@client.event
async def on_message_edit(before, after):
    if not LOADED:
        return
    message = after
    fmt = '**{0.author}** edited their message from: |{1.content}| to |{0.content}|\n'
    if message.server:
        with open(rutil.logpath(message), 'a+') as file:
            file.write(fmt.format(after, before))
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
    else:
        with open(rutil.logpath(message), 'a+') as file:
            file.write(fmt.format(after, before))
            file.write(message.author.name + ": " +
                       message.clean_content + "\n")


@client.event
async def on_message_delete(message):
    if not LOADED:
        return
    if message.server:
        fmt = '{0.author.name} has deleted the message: |{0.content}|\n'
        with open(rutil.logpath(message), 'a+') as file:
            file.write(fmt.format(message))
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
    else:
        fmt = '{0.author.name} has deleted the message: |{0.content}|\n'
        with open(rutil.logpath(message), 'a+') as file:
            file.write(fmt.format(message))
            file.write(message.author.name + ": " +
                       message.clean_content + "\n")


@client.event
async def on_member_join(member):
    if not LOADED:
        return
    if rbot.servers.get('245789672842723329') and member.server is rbot.servers['245789672842723329'].server:
        rutil.eprint("setting team in taboo")
        target = member

        taboo_server = rbot.servers['245789672842723329'].server
        taboo_teams = [
            discord.utils.get(taboo_server.roles, id=teamid)
            for teamid in jfileutil.load("altgen_teams")
        ]

        newteam = taboo_teams[int(target.id) % len(taboo_teams)]
        await client.add_roles(target, newteam)
        await client.send_message(taboo_server.default_channel, "Please welcome " + target.mention + " to " + newteam.name)


async def fear_of_death(freq):
    # global timezone
    while not client.is_closed:
        if (not client.is_logged_in) or (client.is_closed):
            print("Oh no, the client closed???")
            print("Client error. Status: \n\tLogged in: " +
                  str(client.is_logged_in) + "\n\tClosed: " + str(client.is_closed))
            sys.exit()
        await asyncio.sleep(freq)


async def background_check_feed(asyncioloop, blogname, workingChan, rubychan, freq):
    # global timezone
    import time
    mostRecentID = 1
    lastPostID = 0
    update_delay = 0
    time_lastupdate = time.time()
    # Basically run forever
    while not client.is_closed:
        try:
            response = tumblr_client.posts(blogname, limit=1)
            # Get the 'posts' field of the response
            mostRecentPost = response['posts'][0]
            mostRecentID = mostRecentPost['id']

            if mostRecentID != lastPostID:
                if 0 != lastPostID:
                    print(blogname + " change: " +
                          str(lastPostID) + " =/= " + str(mostRecentID))
                    print(blogname + " update: " +
                          str(lastPostID) + " -> " + str(mostRecentID))
                    print("Time since last update: " +
                          str(time.time() - time_lastupdate) + " sec")
                    print("Delay at time of update: " + str(update_delay))
                    time_lastupdate = time.time()
                    update_delay = 0
                    await client.send_message(rubychan, "[[ " + "Update! " + mostRecentPost['post_url'] + "/ ]]")
                    await client.send_message(workingChan, await emote(workingChan.server, 'smolrubes', True) + "[[ Update! ]]")
                elif update_delay < (MAX_UPDATE_DELAY):
                    update_delay += 10
                lastPostID = mostRecentID
                print(lastPostID)
        except:  # TODO: Do not use bare except
            rutil.eprint("error fetching status for " + blogname)
            print(response)
            traceback.print_exc()
            traceback.print_exc(file=sys.stdout)
            # No matter what goes wrong, wait same time and try again
        finally:
            await asyncio.sleep(freq + update_delay)


def rollplain(rolls, limit):
    resultarray = [(random.randint(1, limit)) for r in range(rolls)]
    # result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    resultarray.sort()
    return resultarray


def totalDelimitedList(list, number):
    total = 0
    # array2 = [int(i) for i in list.split(',')]
    array2 = list
    array2.sort()
    array2 = array2[number:]
    for i in array2:
        total += i
    return total


@client.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        print(before.nick + " => " + after.nick)


@client.event
async def on_message(message):
    if not LOADED:
        return
    # tic = time.clock()
    # we do not want the bot to react to itself
    if message.author == client.user:
        return

    if message.server is not None:  # Generic Server
        if "rubybot" in message.content.lower():
            # print("Debug: i've beem nentioned!")
            await client.add_reaction(message, await emote(message.server, 'smolrubes', False))
            # return

        if "boobybot" in message.content.lower():
            # print("Debug: i've beem nentioned!")
            await client.add_reaction(message, await emote(message.server, 'rubyblush', False))
            # return

        if "wwheek" in message.content.lower():
            # print("Debug: i've beem nentioned!")
            await client.add_reaction(message, '💚')
            # return

    if message.server:
        with open(rutil.logpath(message), 'a+') as file:
            file.write("[" + message.channel.name + "] " +
                       message.author.name + ": " + message.clean_content + "\n")
            if message.attachments:
                file.write("[" + message.channel.name + "] " +
                           message.author.name + ": " + str(message.attachments) + "\n")
        for command in rbot.servers[message.server.id].commands:
            # try:
            await command.run(message)
        # except NameError:
        #     await client.send_message(message.channel, "You lack permissions for that operation")

    else:
        with open(rutil.logpath(message), 'a+') as file:
            file.write("[" + message.author.name + "] " +
                       ": " + message.clean_content + "\n")
        for command in rbot.direct_commands:
            await command.run(message)

with open("token", 'rb') as filehandler:
    token = pickle.load(filehandler)

with open("tumblr_token", 'rb') as filehandler:
    tumblr_token_data = pickle.load(filehandler)
    tumblr_client = pytumblr.TumblrRestClient(
        tumblr_token_data[0],
        tumblr_token_data[1],
        tumblr_token_data[2],
        tumblr_token_data[3]
    )

while True:
    try:
        rutil.eprint("Running client")
        client.run(token)
        rutil.eprint("Successful completion?")
    except RuntimeError as e:
        rutil.eprint("Major fault - Runtime error")
        tb = traceback.format_exc()
        tb = tb + "\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rutil.eprint(tb)
        with open("last_trace.log", "w") as f:
            f.write(tb)
            f.flush()
        break
    except SystemExit as e:
        rutil.eprint("Exiting peacefully")
        break
    except BaseException as e:
        rutil.eprint("Major fault - unknown cause")
        tb = traceback.format_exc()
        tb = tb + "\n" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        rutil.eprint(tb)
        with open("last_trace.log", "w") as f:
            f.write(tb)
            f.flush()
        # break

rutil.eprint("Program terminated: Ran over edge of file")
