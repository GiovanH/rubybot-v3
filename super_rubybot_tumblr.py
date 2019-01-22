import time
import asyncio
import pickle
import pytumblr
import traceback
import jfileutil

from snip import ContextPrinter
print = ContextPrinter(vars(), width=20)

MAX_UPDATE_DELAY = 15 * 60  # Fifteen minutes


class TumblrModule():
    def __init__(self, bot, asyncioloop, get_channel):
        super(TumblrModule, self).__init__()
        self.loop = asyncioloop
        self.client = bot
        with open("tumblr_token", 'rb') as filehandler:
            tumblr_token_data = pickle.load(filehandler)
            self.tumblr_client = pytumblr.TumblrRestClient(*tumblr_token_data)
        self.get_channel = get_channel
        self.start()
        print("Ready.")

    def start(self):
        print('Creating update loops')
        tumblr_polls = jfileutil.load("polls")

        for t in tumblr_polls:
            print('Creating update loop for ' + t['blogname'])
            self.loop.create_task(
                self.background_check_feed(
                    self.client,
                    t['blogname'],
                    self.get_channel(t['bigchannel']),
                    self.get_channel(t['minichannel']),
                    t['mindelay']
                )
            )

    async def background_check_feed(self, client, blogname, workingChan, rubychan, freq):
        async def handleUpdate(url):
            await rubychan.send("[[ Update! " + url + " ]]")
            await workingChan.send(await self.client.emotemgr.message(":smolrubes: [[ Update! ]]"))

        mostRecentID = 1
        lastPostID = 0
        update_delay = 0
        time_lastupdate = time.time()
        # Basically run forever
        while not self.loop.is_closed():
            try:
                response = self.tumblr_client.posts(blogname, limit=1)
                # Get the 'posts' field of the response
                mostRecentPost = response['posts'][0]
                mostRecentID = mostRecentPost['id']

                if mostRecentID > lastPostID:
                    if 0 != lastPostID:
                        print(blogname, "change:", lastPostID, "=/=", mostRecentID)
                        print(blogname, "update:", lastPostID, "->", mostRecentID)
                        print("Time since last update:", str(time.time() - time_lastupdate), "sec")
                        print("Delay at time of update:", str(update_delay))
                        time_lastupdate = time.time()
                        update_delay = 0
                        await handleUpdate(mostRecentPost['post_url'])
                    elif update_delay < (MAX_UPDATE_DELAY):
                        update_delay += 10
                    lastPostID = mostRecentID
                    print("Last post at", lastPostID)
            except Exception as e:  # TODO: Do not use bare except
                print("error fetching status for", blogname)
                traceback.print_exc()
                # No matter what goes wrong, wait same time and try again
            finally:
                await asyncio.sleep(freq + update_delay)