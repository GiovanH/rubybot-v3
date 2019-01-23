


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
