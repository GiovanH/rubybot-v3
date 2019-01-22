froggos = []


async def loadfrogs():
    # frogurls = jfileutil.load("frogs")

    # frogfetchers = [
    #     {
    #         "url": "http://allaboutfrogs.org/funstuff/randomfrog.html",
    #         "re": '"(http:\/\/www\.allaboutfrogs\.org\/funstuff\/random\/.*?)"'
    #     },
    #     {
    #         "url": "http://stickyfrogs.tumblr.com/tagged/frogfriends",
    #         "re": 'img src="(.*?)"'
    #     },
    #     {
    #         "url": "https://twitter.com/stickyfrogs/media",
    #         "re": 'img data-aria-label-part src="(.*?)"'
    #     },
    #     {
    #         "url": "https://twitter.com/Litoriacaeru/media",
    #         "re": 'img data-aria-label-part src="(.*?)"'
    #     }
    # ]
    # frogurls = []
    # for method in frogfetchers:
    #     try:
    #         r = urllib.request.urlopen(method['url']).read()
    #         r = r.decode()
    #         frogurls.extend(re.compile(method['re']).findall(r))
    #     except:
    #         traceback.print_exc(file=sys.stdout)
    #         rutil.eprint("frog error, continuing")

    froggos.clear()
    for d in jfileutil.load("frogsmd5"):
        try:
            froggos.append(rbot.Frog(d))
        except Exception as e:
            print("Could not add frog with data " + d)

    # for url in frogurls:
    #     for frog in froggos:
    #         if frog.data['url'] == url:
    #             break
    #     else:
    #         try:
    #             froggos.append(rbot.Frog({'url': url}))
    #         except:
    #             print("Could not add frog with url " + url)
    # save_frogs()


def save_frogs():
    global froggos
    froggos = sorted(list(set(froggos)))
    jfileutil.save([f.data for f in froggos], "frogsmd5")


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
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    await loadCommands()
    global LOADED
    LOADED = True

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
    rbot.Command('pm', cmd_pm_func,
                 'Sends a PM to one person mentioned',  # helpstr
                 3)  # Permission Level

    async def cmd_restart_func(message):
        await client.change_presence(game=discord.Game(name="swords", type=1))
        try:
            await client.add_reaction(message, await emote(message.server, 'smolrubes', False))
        except:
            pass
        rutil.eprint("Restarting rubybot at request of " + message.author.name)
        with open("last_trace.log", "w") as f:
            f.write("Restarted at request of " + message.author.name)
            f.flush()
        sys.exit(0)
    rbot.Command('restart', cmd_restart_func,
                 'Restarts rubybot',  # helpstr
                 2)  # Permission Level
    rbot.Command('reload', cmd_restart_func,
                 'Alias of restart',  # helpstr
                 2)

    async def cmd_smolmote_func(message):
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
        await client.change_nickname(rbot.servers[message.server.id].member, nickname)
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
