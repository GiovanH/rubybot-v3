import discord
from discord.ext import commands
from enum import Enum
import super_rubybot_settings as settings

"""
class Context(discord.abc.Messageable)
 |  Context(**attrs)
 |
 |  Represents the context in which a command is being invoked under.
 |
 |  This class contains a lot of meta data to help you understand more about
 |  the invocation context. This class is not created manually and is instead
 |  passed around to commands as the first parameter.
 |
 |  This class implements the :class:`abc.Messageable` ABC.
 |
 |  Attributes
 |  -----------
 |  message: :class:`discord.Message`
 |      The message that triggered the command being executed.
 |  bot: :class:`.Bot`
 |      The bot that contains the command being executed.
 |  args: :class:`list`
 |      The list of transformed arguments that were passed into the command.
 |      If this is accessed during the :func:`on_command_error` event
 |      then this list could be incomplete.
 |  kwargs: :class:`dict`
 |      A dictionary of transformed arguments that were passed into the command.
 |      Similar to :attr:`args`, if this is accessed in the
 |      :func:`on_command_error` event then this dict could be incomplete.
 |  prefix: :class:`str`
 |      The prefix that was used to invoke the command.
 |  command
 |      The command (i.e. :class:`.Command` or its superclasses) that is being
 |      invoked currently.
 |  invoked_with: :class:`str`
 |      The command name that triggered this invocation. Useful for finding out
 |      which alias called the command.
 |  invoked_subcommand
 |      The subcommand (i.e. :class:`.Command` or its superclasses) that was
 |      invoked. If no valid subcommand was invoked then this is equal to
 |      `None`.
 |  subcommand_passed: Optional[:class:`str`]
 |      The string that was attempted to call a subcommand. This does not have
 |      to point to a valid registered subcommand and could just point to a
 |      nonsense string. If nothing was passed to attempt a call to a
 |      subcommand then this is set to `None`.
 |  command_failed: :class:`bool`
 |      A boolean that indicates if the command failed to be parsed, checked,
 |      or invoked.
 |
 |  Method resolution order:
 |      Context
 |      discord.abc.Messageable
 |      builtins.object
 """
from snip import ContextPrinter
print = ContextPrinter(vars(), width=20)


class Permisison(Enum):
    EVERYONE = 0
    MODERATOR = 1
    ADMIN = 2
    SUPERADMIN = 3


superadmin_ids = [233017800854077441]


class CommandModule(object):
    def __init__(self, bot):
        super(CommandModule, self).__init__()
        bot.add_cog(UtilCog(bot))
        bot.add_cog(FunCog(bot))
        bot.add_cog(InfoCog(bot))
        bot.add_cog(RoleCog(bot))
        bot.add_cog(ModCog(bot))
        bot.add_cog(FrogCog(bot))
        print("Ready.")


def hasPermission(ctx, level):
    aid = ctx.author.id
    if level == Permisison.EVERYONE:
        return True
    if ctx.guild is not None:
        if level == Permisison.ADMIN:
            return ctx.guild.get_member(aid).guild_permissions.administrator
        if level == Permisison.MODERATOR:
            return ctx.guild.get_member(aid).guild_permissions.manage_messages
    if level == Permisison.SUPERADMIN:
        return aid in superadmin_ids
    return False


def permission(level):
    def predicate(ctx):
        return hasPermission(ctx, level)
    return commands.check(predicate)


class Cog():
    def __init__(self, bot):
        self.bot = bot

    # def __init__(self, bot):
    #     super().__init__(bot)

    # async def __before_invoke(self, ctx):
    #     print('Invoking {0.command}'.format(ctx))
    #     ctx.secret_cog_data = 'foo'

    # async def __after_invoke(self, ctx):
    #     print('{0.command} is done.'.format(ctx))


frog_urls = []


def url_to_hash(url):
    import imagehash
    from PIL import Image   # Image IO libraries
    from urllib.request import urlretrieve
    import tempfile

    filename = tempfile.mktemp()
    urlretrieve(url, filename)
    image = Image.open(filename)
    proc_hash = imagehash.dhash(image, hash_size=8)
    return str(proc_hash)


def get_new_frog_urls():
    return [e.get("url") for e in jfileutil.load("frogsmd5")]


class FrogCog(Cog):
    def __init__(self, bot):
        super().__init__(bot)
        self.loadFrogs()

    def loadFrogs(self):
        import jfileutil
        from loom import Spool

        hashedFrogs = jfileutil.load("hashedFrogs", default=dict())

        new_frog_urls = get_new_frog_urls()

        with Spool(4) as hashSpool:
            def job(url):
                phash = url_to_hash(url)
                if phash not in hashedFrogs.keys():
                    hashedFrogs[phash] = url
            for url in new_frog_urls:
                hashSpool.enqueue(target=job, args=(url,))
        jfileutil.save(hashedFrogs, "hashedFrogs")

        global frog_urls
        frog_urls.clear()
        for key in hashedFrogs.keys():
            frog_urls.append(hashedFrogs[key])

    @commands.command(
        brief="acquire FROg",
    )
    @permission(Permisison.EVERYONE)
    async def frog(cog, ctx):
        from random import randint
        frogi = randint(0, len(frog_urls))
        froggo = frog_urls[frogi]
        await ctx.channel.send(
            "[{i}/{t}] Frog for {name}:\n{url}".format(
                i=frogi + 1, t=len(frog_urls) + 1,
                name=ctx.author.name, url=froggo
            )
        )
        
    @commands.command(
        brief="addtitlanl forgs",
    )
    @permission(Permisison.MODERATOR)
    async def addfrog(cog, ctx, url):
        import jfileutil
        hashedFrogs = jfileutil.load("hashedFrogs", default=dict())
        phash = url_to_hash(url)
        if phash not in hashedFrogs.keys():
            hashedFrogs[phash] = url
        jfileutil.save(hashedFrogs, "hashedFrogs")
        await ctx.message.add_reaction("👍")


class ModCog(Cog):
    @commands.command(
        brief="Restrict a user",
        description="Restricts users mentioned. Functionality varies by server.",
        usage="@user [@user2...]",
        aliases=[],
    )
    @permission(Permisison.MODERATOR)
    async def bad(cog, ctx):
        source = ctx.author
        for target in ctx.message.mentions:
            if target is None:
                await ctx.channel.send("No such person")
                await ctx.message.delete()
                return
            bad_roles = map(ctx.guild.get_role, settings.getSetting(ctx.guild.id, "bad").get("bad_roles"))
            good_roles = map(ctx.guild.get_role, settings.getSetting(ctx.guild.id, "bad").get("good_roles"))
            while any(role in target.roles for role in good_roles):
                await target.remove_roles(good_roles)
            while not all(role in target.roles for role in bad_roles):
                await target.add_roles(bad_roles)
            await ctx.channel.send(settings.getSetting(ctx.guild.id, "fmt_bad").format(target=target, source=source))
            # await ctx.channel.send(target.name + " has been badded to the pit by " + source.name + ".")
        await ctx.message.delete

    @commands.command(
        brief="Unrestrict a user",
        description="Reverses action of 'bad'",
        usage="@user [@user2...]",
        aliases=[],
    )
    @permission(Permisison.MODERATOR)
    async def unbad(cog, ctx):
        source = ctx.author
        for target in ctx.message.mentions:
            if target is None:
                await ctx.channel.send("No such person")
                await ctx.message.delete()
                return
            bad_roles = map(ctx.guild.get_role, settings.getSetting(ctx.guild.id, "bad").get("bad_roles"))
            good_roles = map(ctx.guild.get_role, settings.getSetting(ctx.guild.id, "bad").get("good_roles"))
            while any(role in target.roles for role in bad_roles):
                await target.remove_roles(bad_roles)
            while not all(role in target.roles for role in good_roles):
                await target.add_roles(good_roles)
            await ctx.channel.send(settings.getSetting(ctx.guild.id, "fmt_unbad").format(target=target, source=source))
        await ctx.message.delete
        # target.name + " has been unbadded from the pit by " + source.name


class InfoCog(Cog):

    @commands.command(
        brief="Show an arbitrary message",
        description="Shows a server-specific message, titled message_id.",
        help="This powers help, liveblogs, and others. ",
    )
    @permission(Permisison.EVERYONE)
    async def message(cog, ctx, message_id):
        message = settings.getSetting(ctx.guild.id, "messages").get(message_id)
        if message:
            await ctx.channel.send(**message)
        else:
            raise KeyError(message_id)

    @commands.command(
        brief="Show an arbitrary message, without formatting. ",
        description="Shows a server-specific message, titled message_id.",
        help="This powers help, liveblogs, and others. This version is useful for editing.",
    )
    @permission(Permisison.EVERYONE)
    async def mdmessage(cog, ctx, message_id):
        message = settings.getSetting(ctx.guild.id, "messages").get(message_id)
        if message:
            message.content = "```{}```".format(message.content)
            await ctx.channel.send(**message)
        else:
            raise KeyError(message_id)

    @commands.command(
        brief="Set an arbitrary message",
        description="Set a server-specific message with id message_id.",
    )
    @permission(Permisison.MODERATOR)
    async def setmessage(cog, ctx, message_id, *messageWords):
        newMessage = " ".join(messageWords)
        messages = settings.getSetting(ctx.guild.id, "messages")
        messages[message_id] = {"content": newMessage}
        settings.setSetting(ctx.guild.id, "messages", messages)
        await ctx.channel.send("Saved successfully.")

    @commands.command(
        brief="Information about patreon",
        description="please give me some money coins",
        help="my children are starving",
        aliases=["fund"],
    )
    @permission(Permisison.EVERYONE)
    async def patreon(cog, ctx):
        await ctx.channel.send(
            embed=discord.Embed(
                title="Keep me alive and keep Gio healthy!",
                url="https://www.patreon.com/giovan"
            ).set_author(name="Giovan").set_thumbnail(url="https://cdn.discordapp.com/emojis/361958691244867584.png")
        )

    @commands.command()
    @permission(Permisison.EVERYONE)
    async def frig(cog, ctx):
        await ctx.channel.send("http://www.qwantz.com/comics/comic2-1348.png")

    def get_message_alias(self, fixed_message_id):
        async def closure(ctx):
            await ctx.bot.get_command("message").callback(self, ctx, fixed_message_id)
        self.bot.add_command(commands.Command(
            brief="Show the '{}' message".format(fixed_message_id),
            name=fixed_message_id,
            description="description",
            usage="",
            help="help",
            callback=closure
        ))

    def __init__(self, bot):
        super().__init__(bot)
        for fixed_message_id in ["rules", "liveblogs"]:
            self.get_message_alias(fixed_message_id)


class UtilCog(Cog):
    @commands.command(
        brief="Check your permissions",
        description="Shows you what Rubybot permissions you have in this server.",
        aliases=["perms"],
    )
    @permission(Permisison.EVERYONE)
    async def permissions(cog, ctx):
        reply = "Permissions for " + ctx.author.mention + ": \n"
        reply += "```"
        reply += "Super admin: {}\n".format(hasPermission(ctx, Permisison.SUPERADMIN))
        reply += "Admin:       {}\n".format(hasPermission(ctx, Permisison.ADMIN))
        reply += "Moderator:   {}\n".format(hasPermission(ctx, Permisison.MODERATOR))
        reply += "Everyone:    {}\n".format(hasPermission(ctx, Permisison.EVERYONE))
        reply += "```"
        await ctx.message.channel.send(reply)

    @commands.command(
        brief="Check message context",
        description="description",
    )
    @permission(Permisison.SUPERADMIN)
    async def context(cog, ctx):
        from pprint import pprint
        pprint(ctx)
        pprint(dir(ctx))


class RoleCog(Cog):
    @commands.command(
        brief="Toggle active roles",
        description="Grant or revoke specific roles. Use `!togglerole list` for availibility.",
        aliases=["pronoun"],
    )
    @permission(Permisison.EVERYONE)
    async def togglerole(cog, ctx, requested):
        ctx.author = ctx.author
        try:
            freeroles = settings.getSetting(ctx.guild.id, "free_roles")
        except FileNotFoundError:
            await ctx.channel.send("This server has no free roles, or else something is misconfigured.")
        roleLookup = freeroles.get(requested)
        if roleLookup is None:
            await ctx.channel.send("That role name is unknown! Availible roles:")
            await ctx.channel.send("\n".join(["`" + k + "`" for k in freeroles.keys()]))
        else:
            role = ctx.guild.get_role(roleLookup)
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.author.send("You already had the role " + role.name + ", so I'm toggling it off. ")
                print(ctx.author.name + " has role " + role.name + ", removing.")
            else:
                if role not in ctx.author.roles:
                    await ctx.author.add_roles(ctx.author, role)
                    await ctx.author.send("You did not have the role " + role.name + ", so I'm adding it now for you!")
                    print(ctx.author.name + " does not have role " + role.name + ", adding.")


class FunCog(Cog):
    @commands.command(
        brief="Call a vote using reactions",
        description="",
        usage='Option1 "Option 2, a sentance with spaces in it" "Another sentance"',
        help="If you have an option that contains spaces, surround it with quotes.",
        aliases=["vote", "strawpoll", "poll"],
    )
    @permission(Permisison.EVERYONE)
    async def callvote(cog, ctx, *args):
        import random
        options = args
        reactions = random.choice(
            ['🇦🇧🇨🇩🇪🇫🇬🇭', '❤💛💚💙💜🖤💔', '🐶🐰🐍🐘🐭🐸💔', '🍅🍑🍒🍌🍉🍆🍓🍇']
        )
        pollmsg = await ctx.channel.send(".........")
        polltext = ctx.message.author.name + " has called a vote:"
        i = 0
        for o in options:
            polltext = polltext + "\n" + reactions[i] + ": " + o
            print(reactions[i])
            await pollmsg.add_reaction(reactions[i])
            i = i + 1
        await pollmsg.edit(content=polltext)

    @commands.command(
        brief="Rolls fancy dice",
        usage="<x>d<y> [+<z>] [-<a>] [drop<b>]",
        help="Roll a d<y> <x> times. If present, add <z> to the total, subtract <a> from the total, and/or drop the lowest <b> values.",
        aliases=["dx, rollby"],
    )
    @permission(Permisison.EVERYONE)
    async def roll(cog, ctx, dice, *flags):
        from snip import numSplit
        from random import randint
        import traceback
        try:
            (rolls, d, sides) = numSplit(dice)
            (rolls, sides) = map(int, (rolls, sides))
            bonus = 0
            drops = 0
            sort = True
            for flag in flags:
                if flag[0] == "+" or flag[0] == "-":
                    bonus = int(flag[0:])
                if numSplit(flag)[0].lower() == "drop":
                    drops = int(numSplit(flag)[1])
                if flag == "nosort":
                    sort = False
            resultarray = [(randint(1, sides)) for r in range(rolls)]

            if sort:
                resultarray.sort()
                result = ', '.join(str(r) for r in resultarray)
            else:
                result = ', '.join(str(r) for r in resultarray)
                resultarray.sort()

            droparray = resultarray[drops:]
            total = sum(droparray)

            await ctx.message.channel.send(
                "{author.mention}'s roll:\n{result}{totalpart}{droppart}".format(
                    author=ctx.message.author,
                    result=result,
                    totalpart=("\nTotal: `{total} + {bonus} = {tb}`".format(tb=total + bonus, **vars()) if rolls > 1 else ""),
                    droppart=("(Dropped `{}`)".format(", ".join(map(str, resultarray[:drops]))) if drops > 0 else ""),
                    x=None
                ))

        except Exception as e:
            trace = traceback.format_exc()
            print(trace)
            await ctx.message.channel.send("```{}```".format())
            await ctx.message.channel.send("I don't understand the dice notation: " + dice)
