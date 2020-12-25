import html
import json
import os
from typing import Optional

from YuiiChan import (DEV_USERS, OWNER_ID, SUDO_USERS, SUPPORT_CHAT,
                          SUPPORT_USERS, TIGER_USERS, WHITELIST_USERS,
                          dispatcher)
from YuiiChan.modules.helper_funcs.chat_status import (dev_plus, sudo_plus,
                                                           whitelist_plus)
from YuiiChan.modules.helper_funcs.extraction import extract_user
from YuiiChan.modules.log_channel import gloggable
from telegram import ParseMode, TelegramError, Update
from telegram.ext import CallbackContext, CommandHandler, run_async
from telegram.utils.helpers import mention_html

ELEVATED_USERS_FILE = os.path.join(os.getcwd(),
                                   'YuiiChan/elevated_users.json')


def check_user_id(user_id: int, context: CallbackContext) -> Optional[str]:
    bot = context.bot
    if not user_id:
        reply = "That...is a chat! baka ka omae?"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply



# do not async, not a handler
def send_disasters(update):
    update.effective_message.reply_text(
        disasters, parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


@run_async
@dev_plus
@gloggable
def addsudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("This member is already Dev")
        return ""

    if user_id in SUPPORT_USERS:
        rt += "Requested bot Admins to promote."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "Requested bot Admins to promote."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['sudos'].append(user_id)
    SUDO_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully promoted {} to sudo!".format(
            user_member.first_name))

    log_message = (
        f"#SUDO\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addsupport(
    update: Update,
    context: CallbackContext,
) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "Requested bot Admins to promote."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        message.reply_text("This user is already a support user.")
        return ""

    if user_id in WHITELIST_USERS:
        rt += "Requested HA to promote this Wolf Disaster to Demon"
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['supports'].append(user_id)
    SUPPORT_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\n{user_member.first_name} was added as a support user!")

    log_message = (
        f"#SUPPORT\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addwhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "This member is a sudo user, Demoting him."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "This user is already a support user, Demoting him."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        message.reply_text("This user is already a whitelist user.")
        return ""

    data['whitelists'].append(user_id)
    WHITELIST_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a Whitelist User!")

    log_message = (
        f"#WHITELIST\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)} \n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@sudo_plus
@gloggable
def addtiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "This member is a sudo user, Demoting him."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "This user is already a Support user, Demoting him."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "This user is already a Whitelist user, Demoting him."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    if user_id in TIGER_USERS:
        message.reply_text("This user is already a sudo.")
        return ""

    data['tigers'].append(user_id)
    TIGER_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt +
        f"\nSuccessfully promoted {user_member.first_name} to a sudo user!"
    )

    log_message = (
        f"#TIGER\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)} \n"
        f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_plus
@gloggable
def removesudo(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("Requested bot Admins to demote him.")
        SUDO_USERS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUDO\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}"
        )

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(
                chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a Dev user!")
        return ""


@run_async
@sudo_plus
@gloggable
def removesupport(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        message.reply_text("Requested bot Admins to demote him")
        SUPPORT_USERS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNSUPPORT\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Sudo User!")
        return ""


@run_async
@sudo_plus
@gloggable
def removewhitelist(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WHITELIST_USERS:
        message.reply_text("Demoting to normal user")
        WHITELIST_USERS.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNWHITELIST\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Whitelist user!")
        return ""


@run_async
@sudo_plus
@gloggable
def removetiger(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat
    bot, args = context.bot, context.args
    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in TIGER_USERS:
        message.reply_text("Demoting to normal user")
        TIGER_USERS.remove(user_id)
        data['tigers'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (
            f"#UNTIGER\n"
            f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
            f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}"
        )

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Tiger Disaster!")
        return ""


@run_async
@whitelist_plus
def whitelistlist(update: Update, context: CallbackContext):
    reply = "<b>Known whitelist users:</b>\n"
    bot = context.bot
    for each_user in WHITELIST_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def tigerlist(update: Update, context: CallbackContext):
    reply = "<b>Known lesser sudos:</b>\n"
    bot = context.bot
    for each_user in TIGER_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def supportlist(update: Update, context: CallbackContext):
    bot = context.bot
    reply = "<b>Known Support Users:</b>\n"
    for each_user in SUPPORT_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def sudolist(update: Update, context: CallbackContext):
    bot = context.bot
    true_sudo = list(set(SUDO_USERS) - set(DEV_USERS))
    reply = "<b>Known Sudo Users :</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@whitelist_plus
def devlist(update: Update, context: CallbackContext):
    bot = context.bot
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Yui-Chan Club Members ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


__help__ = f"""
 • `/devlist`*:* Lists all dev users.
 • `/sudolist`*:* Lists all sudo users.
 • `/supportlist`*:* Lists all support users.
 • `/whitelistlist`*:* Lists all Whitelist users.
 *Note:* These commands list users with special bot priveleges and can only be used by them.
 You can visit {SUPPORT_CHAT} to query more about these.
"""

SUDO_HANDLER = CommandHandler(("addsudo", "adddragon"), addsudo)
SUPPORT_HANDLER = CommandHandler(("addsupport", "adddemon"), addsupport)
TIGER_HANDLER = CommandHandler(("addtiger"), addtiger)
WHITELIST_HANDLER = CommandHandler(("addwhitelist", "addwolf"), addwhitelist)
UNSUDO_HANDLER = CommandHandler(("removesudo", "removedragon"), removesudo)
UNSUPPORT_HANDLER = CommandHandler(("removesupport", "removedemon"),
                                   removesupport)
UNTIGER_HANDLER = CommandHandler(("removetiger"), removetiger)
UNWHITELIST_HANDLER = CommandHandler(("removewhitelist", "removewolf"),
                                     removewhitelist)

WHITELISTLIST_HANDLER = CommandHandler(["whitelistlist", "wolves"],
                                       whitelistlist)
TIGERLIST_HANDLER = CommandHandler(["tigers"], tigerlist)
SUPPORTLIST_HANDLER = CommandHandler(["supportlist", "demons"], supportlist)
SUDOLIST_HANDLER = CommandHandler(["sudolist", "dragons"], sudolist)
DEVLIST_HANDLER = CommandHandler(["devlist", "heroes"], devlist)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(TIGER_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNTIGER_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(TIGERLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)

__mod_name__ = ""
__handlers__ = [
    SUDO_HANDLER, SUPPORT_HANDLER, TIGER_HANDLER, WHITELIST_HANDLER,
    UNSUDO_HANDLER, UNSUPPORT_HANDLER, UNTIGER_HANDLER, UNWHITELIST_HANDLER,
    WHITELISTLIST_HANDLER, TIGERLIST_HANDLER, SUPPORTLIST_HANDLER,
    SUDOLIST_HANDLER, DEVLIST_HANDLER
]
