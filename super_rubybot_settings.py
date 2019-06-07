from snip import jfileutil

settings_template = {
    "messages": {
        "rules": {
            "content": ""
        }
    },
    "commands": [],
    "liveblogs": "",
    "free_roles": {},
    "bad": {
        "good_roles": [],
        "bad_roles": [],
        "fmt_bad": "{source} {target}",
        "fmt_unbad": "{source} {target}"
    }
}


def settings_filename(guild_id):
    return "settings_{}".format(guild_id)


def getSetting(guild_id, key):
    try:
        settings = jfileutil.load(settings_filename(guild_id))
    except FileNotFoundError:
        print("Missing settings file for server", guild_id)
        settings = settings_template
        jfileutil.save(settings, settings_filename(guild_id))
    try:
        return settings.get(key)
    except KeyError:
        if settings_template.get(key):
            settings[key] = settings_template.get(key)
            jfileutil.save(settings, settings_filename(guild_id))
        else:
            print("No such settings key '{}'".format(key))
            raise


def setSetting(guild_id, key, value):
    try:
        settings = jfileutil.load(settings_filename(guild_id))
    except FileNotFoundError:
        print("Missing settings file for server", guild_id)
        jfileutil.save(settings_template, settings_filename(guild_id))
    try:
        assert settings.get(key)
        settings[key] = value
        jfileutil.save(settings, settings_filename(guild_id))
    except KeyError:
        if settings_template.get(key):
            settings[key] = settings_template.get(key)
            jfileutil.save(settings, settings_filename(guild_id))
        else:
            print("No such settings key '{}'".format(key))
            raise
