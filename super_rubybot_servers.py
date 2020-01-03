import super_rubybot_settings as settings
from discord.ext import commands
import super_rubybot_cmds as SRC

import logging

logger = logging.getLogger(__name__)


class AltServer():
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = bot.get_guild(245789672842723329)
        self.teamids = settings.getSetting(self.guild.id, "altgen_teams")
        self.bind()
        bot.add_cog(AltCog(self)) 
        logger.info("Altgen ready.")

    async def setTeam(self, target):
        if target.guild.id != self.guild.id:
            return

        # print(self.teamids)
        for role in [self.guild.get_role(id_) for id_ in self.teamids]:
            try:
                # print(role)
                await target.remove_roles(role)
            except Exception:
                logger.error("Couldn't remove role", exc_info=True)

        logger.info("setting team in taboo")
        newteam = self.guild.get_role(self.teamids[int(target.id) % len(self.teamids)])
        await target.add_roles(newteam)
        
    def bind(self):
        @self.bot.listen()
        async def on_member_join(member):
            await self.setTeam(member)


class AltCog(SRC.Cog):
    def __init__(self, module):
        super().__init__(bot=module.bot)
        self.guild = module.guild
        self.setTeam = module.setTeam

    @commands.command(
        brief="Reset a user's team."
    )
    @SRC.permission(SRC.Permisison.MODERATOR)
    async def reteam(cog, cxt):
        for target in cxt.message.mentions:
            await cog.setTeam(target)


class LWUServer():
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
        self.guild = bot.get_guild(232218346999775232)
        bot.add_cog(LWUCog(self)) 
        logger.info("LWU ready.")
        

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
