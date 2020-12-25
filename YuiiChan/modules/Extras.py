import random
import re
import json
import html
import urllib.request
import urllib.parse
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError


from telegram import Message, Chat, Update, Bot, ParseMode
from telegram.ext import run_async

from YuiiChan import dispatcher
from YuiiChan.modules.disable import DisableAbleCommandHandler
import YuiiChan.modules.fun_strings as fun_strings
from YuiiChan.modules.helper_funcs.chat_status import (is_user_admin)
from YuiiChan.modules.helper_funcs.extraction import extract_user
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

@run_async
def runs(update: Update, context: CallbackContext):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))


@run_async
def slap(update: Update, context: CallbackContext):
    bot, args = context.bot, context.args
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_SAITAMA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(
                    chat.id,
                    message.from_user.id,
                    until_date=mutetime,
                    permissions=ChatPermissions(can_send_messages=False))
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    reply = temp.format(
        user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
def roll(update: Update, context: CallbackContext):
    update.message.reply_text(random.choice(range(1, 7)))

@run_async
def rlg(update: Update, context: CallbackContext):
    eyes = random.choice(fun_strings.EYES)
    mouth = random.choice(fun_strings.MOUTHS)
    ears = random.choice(fun_strings.EARS)

    if len(eyes) == 2:
       repl = ears[0] + eyes[0] + mouth[0] + eyes[1] + ears[1]
    else:
       repl = ears[0] + eyes[0] + mouth[0] + eyes[0] + ears[1]
    update.message.reply_text(repl)

@run_async
def table(update: Update, context: CallbackContext):
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text(random.choice(fun_strings.TABLE))


SHRUGS = (
    "┐(´д｀)┌",
    "┐(´～｀)┌",
    "┐(´ー｀)┌",
    "┐(￣ヘ￣)┌",
    "╮(╯∀╰)╭",
    "╮(╯_╰)╭",
    "┐(´д`)┌",
    "┐(´∀｀)┌",
    "ʅ(́◡◝)ʃ",
    "┐(ﾟ～ﾟ)┌",
    "┐('д')┌",
    "┐(‘～`;)┌",
    "ヘ(´－｀;)ヘ",
    "┐( -“-)┌",
    "ʅ（´◔౪◔）ʃ",
    "ヽ(゜～゜o)ノ",
    "ヽ(~～~ )ノ",
    "┐(~ー~;)┌",
    "┐(-。ー;)┌",
    r"¯\_(ツ)_/¯",
    r"¯\_(⊙_ʖ⊙)_/¯",
    r"¯\_༼ ಥ ‿ ಥ ༽_/¯",
    "乁( ⁰͡  Ĺ̯ ⁰͡ ) ㄏ",
)

HUGS = (
"⊂(・﹏・⊂)",
"⊂(・ヮ・⊂)",
"⊂(・▽・⊂)",
"(っಠ‿ಠ)っ",
"ʕっ•ᴥ•ʔっ",
"（っ・∀・）っ",
"(っ⇀⑃↼)っ",
"(つ´∀｀)つ",
"(.づσ▿σ)づ.",
"⊂(´・ω・｀⊂)",
"(づ￣ ³￣)づ",
"(.づ◡﹏◡)づ.",
)

TOSS = (
"The coin landed on heads.",
"The coin landed on tails."
)

REACTS = (
    "ʘ‿ʘ",
    "ヾ(-_- )ゞ",
    "(っ˘ڡ˘ς)",
    "(´ж｀ς)",
    "( ಠ ʖ̯ ಠ)",
    "(° ͜ʖ͡°)╭∩╮",
    "(ᵟຶ︵ ᵟຶ)",
    "(งツ)ว",
    "ʚ(•｀",
    "(っ▀¯▀)つ",
    "(◠﹏◠)",
    "( ͡ಠ ʖ̯ ͡ಠ)",
    "( ఠ ͟ʖ ఠ)",
    "(∩｀-´)⊃━☆ﾟ.*･｡ﾟ",
    "(⊃｡•́‿•̀｡)⊃",
    "(._.)",
    "{•̃_•̃}",
    "(ᵔᴥᵔ)",
    "♨_♨",
    "⥀.⥀",
    "ح˚௰˚づ ",
    "(҂◡_◡)",
    "ƪ(ړײ)‎ƪ​​",
    "(っ•́｡•́)♪♬",
    "◖ᵔᴥᵔ◗ ♪ ♫ ",
    "(☞ﾟヮﾟ)☞",
    "[¬º-°]¬",
    "(Ծ‸ Ծ)",
    "(•̀ᴗ•́)و ̑̑",
    "ヾ(´〇`)ﾉ♪♪♪",
    "(ง'̀-'́)ง",
    "ლ(•́•́ლ)",
    "ʕ •́؈•̀ ₎",
    "♪♪ ヽ(ˇ∀ˇ )ゞ",
    "щ（ﾟДﾟщ）",
    "( ˇ෴ˇ )",
    "눈_눈",
    "(๑•́ ₃ •̀๑) ",
    "( ˘ ³˘)♥ ",
    "ԅ(≖‿≖ԅ)",
    "♥‿♥",
    "◔_◔",
    "⁽⁽ଘ( ˊᵕˋ )ଓ⁾⁾",
    "乁( ◔ ౪◔)「      ┑(￣Д ￣)┍",
    "( ఠൠఠ )ﾉ",
    "٩(๏_๏)۶",
    "┌(ㆆ㉨ㆆ)ʃ",
    "ఠ_ఠ",
    "(づ｡◕‿‿◕｡)づ",
    "(ノಠ ∩ಠ)ノ彡( \\o°o)\\",
    "“ヽ(´▽｀)ノ”",
    "༼ ༎ຶ ෴ ༎ຶ༽",
    "｡ﾟ( ﾟஇ‸இﾟ)ﾟ｡",
    "(づ￣ ³￣)づ",
    "(⊙.☉)7",
    "ᕕ( ᐛ )ᕗ",
    "t(-_-t)",
    "(ಥ⌣ಥ)",
    "ヽ༼ ಠ益ಠ ༽ﾉ",
    "༼∵༽ ༼⍨༽ ༼⍢༽ ༼⍤༽",
    "ミ●﹏☉ミ",
    "(⊙_◎)",
    "¿ⓧ_ⓧﮌ",
    "ಠ_ಠ",
    "(´･_･`)",
    "ᕦ(ò_óˇ)ᕤ",
    "⊙﹏⊙",
    "(╯°□°）╯︵ ┻━┻",
    r"¯\_(⊙︿⊙)_/¯",
    "٩◔̯◔۶",
    "°‿‿°",
    "ᕙ(⇀‸↼‶)ᕗ",
    "⊂(◉‿◉)つ",
    "V•ᴥ•V",
    "q(❂‿❂)p",
    "ಥ_ಥ",
    "ฅ^•ﻌ•^ฅ",
    "ಥ﹏ಥ",
    "（ ^_^）o自自o（^_^ ）",
    "ಠ‿ಠ",
    "ヽ(´▽`)/",
    "ᵒᴥᵒ#",
    "( ͡° ͜ʖ ͡°)",
    "┬─┬﻿ ノ( ゜-゜ノ)",
    "ヽ(´ー｀)ノ",
    "☜(⌒▽⌒)☞",
    "ε=ε=ε=┌(;*´Д`)ﾉ",
    "(╬ ಠ益ಠ)",
    "┬─┬⃰͡ (ᵔᵕᵔ͜ )",
    "┻━┻ ︵ヽ(`Д´)ﾉ︵﻿ ┻━┻",
    "ʕᵔᴥᵔʔ",
    "(`･ω･´)",
    "ʕ•ᴥ•ʔ",
    "ლ(｀ー´ლ)",
    "ʕʘ̅͜ʘ̅ʔ",
    "（　ﾟДﾟ）",
    r"¯\(°_o)/¯",
    "(｡◕‿◕｡)",
)

normiefont = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
weebyfont = ['卂','乃','匚','刀','乇','下','厶','卄','工','丁','长','乚','从','𠘨','口','尸','㔿','尺','丂','丅','凵','リ','山','乂','丫','乙']


@run_async
def shrug(update: Update, context: CallbackContext):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text = reply_text(random.choice(SHRUGS))

run_async
def bluetext(update: Update, context: CallbackContext):
    msg = update.effective_message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text
    reply_text(
        "/BLUE /TEXT\n/MUST /CLICK\n/I /AM /A /STUPID /ANIMAL /THAT /IS /ATTRACTED /TO /COLORS"
    )

@run_async
def hug(update: Update, context: CallbackContext):
    # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text = reply_text(random.choice(HUGS))


@run_async
def toss(update: Update, context: CallbackContext):
 	update.effective_message.reply_text(random.choice(TOSS))


@run_async
def react(update: Update, context: CallbackContext):
	 # reply to correct message
    reply_text = update.effective_message.reply_to_message.reply_text if update.effective_message.reply_to_message else update.effective_message.reply_text
    reply_text = reply_text(random.choice(REACTS))


@run_async
def shout(update: Update, context: CallbackContext):
    msg = "```"
    text = context.args
    result = []
    result.append(' '.join([s for s in text]))
    for pos, symbol in enumerate(text[1:]):
        result.append(symbol + ' ' + '  ' * pos + symbol)
    result = list("\n".join(result))
    result[0] = text[0]
    result = "".join(result)
    result = str(result).upper()
    msg = "```\n" + result + "```"
    return update.effective_message.reply_text(msg, parse_mode="MARKDOWN")


@run_async
def pat(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = str(update.message.text)
    try:
        msg = msg.split(" ", 1)[1]
    except IndexError:
        msg = ""
    msg_id = update.effective_message.reply_to_message.message_id if update.effective_message.reply_to_message else update.effective_message.message_id
    pats = []
    pats = json.loads(urllib.request.urlopen(urllib.request.Request(
    'http://headp.at/js/pats.json',
    headers={'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) '
         'Gecko/20071127 Firefox/2.0.0.11'}
    )).read().decode('utf-8'))
    if "@" in msg and len(msg) > 5:
        context.bot.send_photo(chat_id, f'https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}', caption=msg)
    else:
        context.bot.send_photo(chat_id, f'https://headp.at/pats/{urllib.parse.quote(random.choice(pats))}', reply_to_message_id=msg_id)


@run_async
def wiki(update: Update, context: CallbackContext):
    msg = update.effective_message.reply_to_message if update.effective_message.reply_to_message else update.effective_message
    res = ""
    if msg == update.effective_message:
        search = msg.text.split(" ", maxsplit=1)[1]
    else:
        search = msg.text
    try:
        res = wikipedia.summary(search)
    except DisambiguationError as e:
        update.message.reply_text("Disambiguated pages found! Adjust your query accordingly.\n<i>{}</i>".format(e),
        parse_mode=ParseMode.HTML)
    except PageError as e:
        update.message.reply_text("<code>{}</code>".format(e), parse_mode=ParseMode.HTML)
    if res:
        result = f"<b>{search}</b>\n\n"
        result += f"<i>{res}</i>\n"
        result += f"""<a href="https://en.wikipedia.org/wiki/{search.replace(" ", "%20")}">Read more...</a>"""
        if len(result) > 4000:
            with open("result.txt", 'w') as f:
                f.write(f"{result}\n\nUwU OwO OmO UmU")
            with open("result.txt", 'rb') as f:
                context.bot.send_document(document=f, filename=f.name,
                    reply_to_message_id=update.message.message_id, chat_id=update.effective_chat.id,
                    parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(result, parse_mode=ParseMode.HTML)


@run_async
def judge(update: Update, context: CallbackContext):
    judger = ["<b>is lying!</b>", "<b>is telling the truth!</b>"]
    rep = update.effective_message
    msg = ""
    msg = update.effective_message.reply_to_message
    if not msg:
        rep.reply_text("Reply to someone's message to judge them!")
    else:
        user = msg.from_user.first_name
    res = random.choice(judger)
    reply = msg.reply_text(f"{user} {res}", parse_mode=ParseMode.HTML)


@run_async
def weebify(update: Update, context: CallbackContext):
    msg = update.effective_message
    args = msg.text.strip().split(" ", 1)
    if args:
        string = str(args[1]).lower()
    elif msg.reply_to_message:
        string = msg.reply_to_message.text.lower()
    else:
        msg.reply_text("Enter some text to weebify or reply to someone's message!")
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            weebycharacter = weebyfont[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, weebycharacter)

    if msg.reply_to_message:
        msg.reply_to_message.reply_text(string)
    else:
        msg.reply_text(string)



__help__ = """
-  /runs: reply a random string from an array of replies.
-  /slap: slap a user, or get slapped if not a reply.
 - /shg or /shrug: pretty self-explanatory.
 - /hug: give a hug and spread the love :)
 - /pat: give a headpat :3
 - /react: send a random reaction.
 - /toss: toss a coin.
 - /bluetext: check urself :V
 - /rlg: Join ears,nose,mouth and create an emo ;-;
 - /table: get flip/unflip :v.
 - /wiki <term>: do a search on Wikipedia.
 - /judge: as a reply to someone, checks if they're lying or not!
 - /weebify: as a reply to a message, "weebifies" the message.
"""

SHRUG_HANDLER = DisableAbleCommandHandler(["shrug", "shg"], shrug)
RUNS_HANDLER = DisableAbleCommandHandler("runs", runs)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap)
BLUETEXT_HANDLER = DisableAbleCommandHandler("bluetext", bluetext)
RLG_HANDLER = DisableAbleCommandHandler("rlg", rlg)
HUG_HANDLER = DisableAbleCommandHandler("hug", hug)
REACT_HANDLER = DisableAbleCommandHandler("react", react)
TOSS_HANDLER = DisableAbleCommandHandler("toss", toss)
#SHOUT_HANDLER = DisableAbleCommandHandler("shout", shout, pass_args=True)
PAT_HANDLER = DisableAbleCommandHandler("pat", pat)
WIKI_HANDLER = DisableAbleCommandHandler("wiki", wiki)
JUDGE_HANDLER = DisableAbleCommandHandler(["judge", "decide"], judge)
TABLE_HANDLER = DisableAbleCommandHandler("table", table)
WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify, pass_args=True)
ROLL_HANDLER = DisableAbleCommandHandler("roll", roll)

dispatcher.add_handler(SHRUG_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(REACT_HANDLER)
#dispatcher.add_handler(SHOUT_HANDLER)
dispatcher.add_handler(TOSS_HANDLER)
dispatcher.add_handler(PAT_HANDLER)
dispatcher.add_handler(WIKI_HANDLER)
dispatcher.add_handler(JUDGE_HANDLER)
dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(TABLE_HANDLER)
dispatcher.add_handler(BLUETEXT_HANDLER)
dispatcher.add_handler(RLG_HANDLER)
dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
dispatcher.add_handler(ROLL_HANDLER)

__mod_name__ = "Extras"

__command_list__ = [
    "runs", "slap", "shrug", "hug","pat","react","toss", "shg", "bluetext", "rlg", "judge",
    "table","shout","wiki"
]
__handlers__ = [
    RUNS_HANDLER, SLAP_HANDLER, ROLL_HANDLER, TOSS_HANDLER, SHRUG_HANDLER,
    BLUETEXT_HANDLER, RLG_HANDLER, TABLE_HANDLER, WEEBIFY_HANDLER,
    JUDGE_HANDLER, WIKI_HANDLER, PAT_HANDLER, HUG_HANDLER, REACT_HANDLER
]
