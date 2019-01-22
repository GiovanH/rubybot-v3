import super_rubybot_settings as settings
from snip import ContextPrinter
from discord.ext import commands
import super_rubybot_cmds as SRC
print = ContextPrinter(vars(), width=20)


class AltServer():
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = bot.get_guild(245789672842723329)
        self.teamids = settings.getSetting(self.guild.id, "altgen_teams")
        self.bind()
        bot.add_cog(AltCog(self)) 
        print("Altgen ready.")
        
    def bind(self):
        @self.bot.listen()
        async def on_member_join(member):
            if member.guild.id != self.guild.id:
                return
            print("setting team in taboo")
            newteam = self.guild.get_role(self.teamids[int(member.id) % len(self.teamids)])
            await member.add_roles(newteam)


class AltCog(SRC.Cog):
    def __init__(self, module):
        super().__init__(bot=module.bot)
        self.guild = module.guild
        self.teamids = module.teamids

    @commands.command(
        brief="Reset a user's team."
    )
    @SRC.permission(SRC.Permisison.MODERATOR)
    async def reteam(cog, cxt):
        teamids = settings.getSetting(cxt.guild.id, "altgen_teams")
        for target in cxt.message.mentions:
            target.remove_roles([cxt.guild.get_role(id_) for id_ in teamids])
            newteam = cxt.guild.get_role(teamids[int(target.id) % len(teamids)])
            await target.add_roles(newteam)


class LWUServer():
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = bot.get_guild(232218346999775232)
        bot.add_cog(LWUCog(self)) 
        print("LWU ready.")
        

class LWUCog(SRC.Cog):
    def __init__(self, module):
        super().__init__(bot=module.bot)
        self.guild = module.guild

    @commands.command(
        brief="Verify a new user."
    )
    @SRC.permission(SRC.Permisison.MODERATOR)
    async def verify(cog, ctx):
        # workingChan = ctx.guild.get_channel(388730628176084992)
        verified = ctx.guild.get_role(388737413213716481)
        for member in ctx.message.mentions:
            if verified not in member.roles:
                await member.add_roles(verified)
                await ctx.channel.send("Verified user " + member.name)
            else:
                await ctx.channel.send("User is already verified: " + member.name)
        # await workingChan.send("Please welcome new user " + member.mention + " to the server!")
        # await ctx.message.delete()