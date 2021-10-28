"""File Converter
.nfc """
import asyncio
import logging
import os
import time
from datetime import datetime

from sample_config import Config
from userbot import bot
from userbot.util import admin_cmd, progress, run_command

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@bot.on(admin_cmd(pattern="nfc (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    if reply_message is None:
        await event.edit("reply to a media to use the `nfc` operation.\nInspired by @FileConverterBot")
        return
    await event.edit("trying to download media file, to my local")
    try:
        start = datetime.now()
        c_time = time.time()
        downloaded_file_name = await bot.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download")
            )
        )
    except Exception as e:  # pylint:disable=C0103,W0703
        await event.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        new_required_file_name = ""
        new_required_file_caption = ""
        command_to_run = []
        voice_note = False
        supports_streaming = False
        if input_str == "voice":
            new_required_file_caption = "NLFC_" + \
                str(round(time.time())) + ".opus"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + \
                "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-map",
                "0:a",
                "-codec:a",
                "libopus",
                "-b:a",
                "100k",
                "-vbr",
                "on",
                new_required_file_name
            ]
            voice_note = True
            supports_streaming = True
        elif input_str == "mp3":
            new_required_file_caption = "NLFC_" + \
                str(round(time.time())) + ".mp3"
            new_required_file_name = Config.TMP_DOWNLOAD_DIRECTORY + \
                "/" + new_required_file_caption
            command_to_run = [
                "ffmpeg",
                "-i",
                downloaded_file_name,
                "-vn",
                new_required_file_name
            ]
            voice_note = False
            supports_streaming = True
        else:
            await event.edit("not supported")
            os.remove(downloaded_file_name)
            return
        logger.info(command_to_run)
        t_response, e_response = await run_command(command_to_run)
        os.remove(downloaded_file_name)
        if os.path.exists(new_required_file_name):
            end_two = datetime.now()
            force_document = False
            await bot.send_file(
                entity=event.chat_id,
                file=new_required_file_name,
                allow_cache=False,
                silent=True,
                force_document=force_document,
                voice_note=voice_note,
                supports_streaming=supports_streaming,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, event, c_time, "trying to upload")
                )
            )
            ms_two = (end_two - end).seconds
            os.remove(new_required_file_name)
            await event.edit(f"converted in {ms_two} seconds")
