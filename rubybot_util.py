import datetime

client = {}

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

async def send_message_smart(dest, msg):
    m = ""
    for line in msg.split('\n'):
        m += line + "\n"
        if len(m) >= 1600:
            await client.send_message(dest, m)
            m = ""
    await client.send_message(dest, m)

def eprint(*args, **kwargs):
    # global gio
    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(t, file=sys.stderr, **kwargs)
    # print(*args, file=sys.stderr, **kwargs)
    print("[Logging:]" + t)
    print(*args, **kwargs)
    # await client.send_message(gio, *args)
