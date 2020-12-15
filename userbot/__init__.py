# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot initialization. """


from sample_config import Config
from telethon import TelegramClient

from ..scripts.generate_mongo_session import session

if session:
    bot = TelegramClient(session, Config.APP_ID, Config.API_HASH)
else:
    bot = TelegramClient("userbot", Config.APP_ID, Config.API_HASH)

if Config.TG_BOT_TOKEN_BF_HER:
    tgbot = TelegramClient("bot", Config.APP_ID, Config.API_HASH).start(
        bot_token=Config.TG_BOT_TOKEN_BF_HER)


# Global Variables
COUNT_MSG = 0
USERS = {}
COUNT_PM = {}
LASTMSG = {}
CMD_HELP = {}
AFKREASON = "no reason"
