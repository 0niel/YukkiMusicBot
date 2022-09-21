#
# Copyright (C) 2021-2022 by TeamYukki@Github, < https://github.com/TeamYukki >.
#
# This file is part of < https://github.com/TeamYukki/YukkiMusicBot > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TeamYukki/YukkiMusicBot/blob/master/LICENSE >
#
# All rights reserved.

import asyncio
from datetime import datetime
from pyrogram import enums

import config
from YukkiMusic import app
from YukkiMusic.core.call import Yukki, autoend
from YukkiMusic.utils.database import (get_client, is_active_chat,
                                       is_autoend)


async def auto_leave():
    if config.AUTO_LEAVING_ASSISTANT != str(True):
        return
    while not await asyncio.sleep(
        config.AUTO_LEAVE_ASSISTANT_TIME
    ):
        from YukkiMusic.core.userbot import assistants

        for num in assistants:
            client = await get_client(num)
            left = 0
            try:
                async for i in client.get_dialogs():
                    chat_type = i.chat.type
                    if chat_type in [
                        enums.ChatType.SUPERGROUP,
                        enums.ChatType.GROUP,
                        enums.ChatType.CHANNEL,
                    ]:
                        chat_id = i.chat.id
                        if chat_id not in [config.LOG_GROUP_ID, -1001190342892, -1001733534088, -1001443281821]:
                            if left == 20:
                                continue
                            if not await is_active_chat(chat_id):
                                try:
                                    await client.leave_chat(
                                        chat_id
                                    )
                                    left += 1
                                except Exception:
                                    continue
            except Exception:
                pass


asyncio.create_task(auto_leave())


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await Yukki.stop_stream(chat_id)
                except Exception:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "Bot has left voice chat due to inactivity to avoid overload on servers. No-one was listening to the bot on voice chat.",
                    )
                except Exception:
                    continue


asyncio.create_task(auto_end())
