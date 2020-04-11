import time
import asyncio
import pickle
import pytumblr
import traceback
import os
import time
from snip import jfileutil

import threading

from snip.stream import TriadLogger

logger = TriadLogger(__name__)

MAX_UPDATE_DELAY = 4 * 60  # Four minutes


class TumblrModule():
    def __init__(self, bot, get_channel):
        super(TumblrModule, self).__init__()
        self.loop = asyncio.get_event_loop()
        self.client = bot
        with open("tumblr_token", 'rb') as filehandler:
            tumblr_token_data = pickle.load(filehandler)
            self.tumblr_client = pytumblr.TumblrRestClient(*tumblr_token_data)
        self.get_channel = get_channel
        self.start()
        logger.info("Ready.")

    def start(self):
        logger.info('Creating update loops')
        tumblr_polls = jfileutil.load("polls")

        for t in tumblr_polls:
            logger.info('Creating update loop for ' + t['blogname'])
            self.loop.create_task(
                self.background_check_feed(
                    self.client,
                    t['blogname'],
                    self.client.get_channel(t['bigchannel']),
                    self.client.get_channel(t['minichannel']),
                    t['mindelay']
                )
            )

    async def background_check_feed(self, client, blogname, workingChan, rubychan, freq):
        checker = f"{blogname}@{os.getpid()}.{time.time()}"
        
        async def handleUpdate(url):
            if rubychan:
                await rubychan.send("[[ Update! " + url + " ]]")
            if workingChan:
                await workingChan.send("[[ Update! ]]")

        mostRecentID = 1
        lastPostID = 0
        update_delay = 0
        time_lastupdate = time.time()

        this_lock = threading.Lock()

        # Basically run forever
        while not self.loop.is_closed():
            try:
                with this_lock:
                    response = self.tumblr_client.posts(blogname, limit=1)
                    # Get the 'posts' field of the response
                    if not response.get("posts"):  # Intentionally catching the empty list, here
                        logger.error(f"{checker} {blogname} Bad response from tumblr")
                        raise KeyError(response)

                    recent_posts = response['posts']
                    recent_posts.reverse()

                    for post in recent_posts:
                        if post['id'] > lastPostID:

                            # mostRecentPost = response['posts'][0]
                            mostRecentID = post['id']

                            # if mostRecentID > lastPostID:
                            if 0 == lastPostID:
                                lastPostID = mostRecentID
                                continue

                            logger.debug(f"{checker} {blogname} update: {lastPostID} -> {mostRecentID}")
                            logger.debug(repr([p['id'] for p in recent_posts]))
                            
                            print(blogname, "Time since last update:", str(time.time() - time_lastupdate), "sec")
                            print("Delay at time of update:", freq, "+", update_delay)
                            time_lastupdate = time.time()
                            
                            update_delay = 0

                            lastPostID = mostRecentID
                            logger.debug(f"{checker} {blogname} last post is now id {lastPostID}, should be {mostRecentID}")

                            logger.info(f"{blogname} Broadcasting update {mostRecentID}")
                            await handleUpdate(post['post_url'])

                        elif update_delay < (MAX_UPDATE_DELAY):
                            update_delay += 1
            except Exception:  # TODO: Do not use bare except
                logger.error(f"error fetching status for {blogname}", exc_info=True)
                
                # No matter what goes wrong, wait same time and try again
            finally:
                await asyncio.sleep(freq + update_delay)
