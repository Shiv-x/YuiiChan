import platform
import asyncio
import shutil
from telegram import ParseMode
import sys
from YuiiChan import dispatcher
from telegram.ext import CallbackContext, run_async, CommandHandler
from YuiiChan.modules.helper_funcs.chat_status import sudo_plus
import telethon
import telegram
from telegram import Update

@run_async
@sudo_plus
def sysinfo(update: Update, context: CallbackContext):
        chat = update.effective_chat
        msg = update.effective_message
        reply = "**System Info**"
        reply += "\n**Kernal:** {}".format(platform.release())
        reply += "\n**Arch:** {}".format(platform.architecture()[0])
        reply += "\n**OS:** {}".format(platform.system())

        if platform.system() == "Linux":
            done = False
            try:
                a = open("/etc/os-release").readlines()
                b = {}
                for line in a:
                    b[line.split("=")[0]] = line.split("=")[1].strip().strip("\"")
                reply += "\n**Linux Distribution:** {}".format(b["PRETTY_NAME"])
                done = True
            except FileNotFoundError:
                getprop = shutil.which("getprop")
                if getprop is not None:
                    sdk = asyncio.create_subprocess_exec(getprop, "ro.build.version.sdk",
                                                               stdout=asyncio.subprocess.PIPE)
                    ver = asyncio.create_subprocess_exec(getprop, "ro.build.version.release",
                                                               stdout=asyncio.subprocess.PIPE)
                    sec = asyncio.create_subprocess_exec(getprop, "ro.build.version.security_patch",
                                                               stdout=asyncio.subprocess.PIPE)
                    sdks, unused = sdk.communicate()
                    vers, unused = ver.communicate()
                    secs, unused = sec.communicate()
                    if sdk.returncode == 0 and ver.returncode == 0 and sec.returncode == 0:
                        reply += "\n**Android SDK**: {}".format(sdks.decode("utf-8").strip())
                        reply += "\n**Android Version:** {}".format(vers.decode("utf-8").strip())
                        reply += "\n**Android Security Patch:** {}".format(secs.decode("utf-8").strip())
                        done = True
            if not done:
                reply += "\nCould not determine Linux distribution."
        reply += "\n**Python version:** {}".format(sys.version)
        
        reply += "\n**Python-telegram-bot version:** {}".format(telegram.__version__)
        reply += "\n**Telethon version:** {}".format(telethon.__version__)
        msg.reply_text(reply, parse_mode=ParseMode.MARKDOWN)

SYSINFO = CommandHandler("sysinfo", sysinfo)

dispatcher.add_handler(SYSINFO)
