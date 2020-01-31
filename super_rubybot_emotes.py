
from snip.stream import TriadLogger

logger = TriadLogger(__name__)

# EMOTES = {
#     "question": 537010720324190233
# }


class EmoteManager(object):
    def __init__(self, client):
        super(EmoteManager, self).__init__()
        self.client = client
        self.emotes = {}
        print("Ready.")

    async def messsage(self, message):
        return message

    async def emote(self, guild, emotename, braces):
        emojis = self.client.emojis
        fallback_name = "smolrubes"
        fallback = None
        for emoji in emojis:
            if emoji.guild_id == guild.id:
                if emoji.name == emotename:
                    return emoji
                elif emoji.name == fallback_name:
                    fallback = emoji

        else:
            if fallback:
                logger.warning("Using fallback emoji in", guild)
                return fallback
            else:
                if self.client.get_member(guild).guild_permissions.manage_emojis:
                    with open("asset/" + fallback_name + ".png", 'rb') as fp:
                        logger.warning("I'm being forced to add an emoji to " + guild.name)
                        return await guild.create_custom_emoji(name=fallback_name, image=fp.read())

            logger.error("EMOJI FAILURE! Guild: '{guild.name}' <{guild.id}>, Manage emojis permission: {manage}".format(
                guild=guild,
                manage=self.client.get_member(guild).guild_permissions.manage_emojis
            ))
            return "?"
