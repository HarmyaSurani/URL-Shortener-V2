import uvloop
uvloop.install()
import datetime
import logging
import logging.config
import sys

from pyrogram import Client


from config import *
from config import UPDATE_CHANNEL
from database import db
from database.users import filter_users
from helpers import temp
from utils import broadcast_admins, create_server, set_commands

# Get logging configurations
logging.config.fileConfig("logging.conf")
logging.getLogger().setLevel(logging.INFO)


class Bot(Client):
    def __init__(self):
        super().__init__(
            "shortener",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins"),
        )

    async def start(self):

        temp.START_TIME = datetime.datetime.now()
        await super().start()

        if UPDATE_CHANNEL:
try:
                self.invite_link = (await self.get_chat(UPDATE_CHANNEL)).invite_link
                if not link:
                    await self.export_chat_invite_link(UPDATB_CHANNEL)
                    self.invite_link = (await self.get_chat(UPDATE_CHANNEL)).invite_link
                self.invitelink = self.invite_link
            except Exception as a:
                self.LOGGER(__name__).warning(a)
                self.LOGGER(__name__).warning("Bot can't Export Invite link from Force Sub Channel!")
                self.LOGGER(__name__).warning(f"Please Double check the FORCE_SUB_CHANNEL value and Make sure Bot is Admin in channel with Invite Users via Link Permission, Current Force Sub Channel Value: {FORCE_SUB_CHANNEL}")
                self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/CodeXBotzSupport for support")
                sys.exit()
        
        temp.START_TIME = datetime.datetime.now()
        await super().start()

        me = await self.get_me()
        self.owner = await self.get_users(int(OWNER_ID))
        self.username = f"@{me.username}"
        temp.BOT_USERNAME = me.username
        temp.FIRST_NAME = me.first_name
        if not await db.get_bot_stats():
            await db.create_stats()

        banned_users = await filter_users({"banned": True})
        async for user in banned_users:
            temp.BANNED_USERS.append(user["user_id"])

        await set_commands(self)

        await broadcast_admins(self, "** Bot started successfully **")
        logging.info("Bot started")

        if WEB_SERVER:
            await create_server()
            logging.info("Web server started")
            logging.info("Pinging server")

    async def stop(self):
        await broadcast_admins(self, "** Bot Stopped Bye **")
        await super().stop()
        logging.info("Bot Stopped Bye")
