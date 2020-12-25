import requests
import os
from YuiiChan import dispatcher
from YuiiChan.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async


@run_async
def paste(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message
    if not message.reply_to_message:
        try:
          data = message.text.split(None, 1)[1]
        except:
          message.reply_text("What am I supposed to paste?")
          return
    else:

      if message.reply_to_message.text:
          data = message.reply_to_message.text
    
      elif message.reply_to_message.document:
        document_id = message.reply_to_message.document.file_id
        file = context.bot.get_file(document_id)
        file.download("paste.txt")
        with open("paste.txt", "rb") as fd:
                m_list = fd.readlines()
                data = ""
                for m in m_list:
                    data += m.decode("UTF-8")
        os.remove("paste.txt")
        
      else:
        message.reply_text("Error parsing paste content.")
        return

    key = requests.post(
        'https://nekobin.com/api/documents', json={
            "content": data
        }).json().get('result').get('key')

    url = f'https://nekobin.com/{key}'

    reply_text = f'Nekofied to *Nekobin* : {url}'

    message.reply_text(
        reply_text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True)


__help__ = """
 • `/paste`*:* Do a paste at `neko.bin`
"""

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste)
dispatcher.add_handler(PASTE_HANDLER)

__mod_name__ = "Paste"
__command_list__ = ["paste"]
__handlers__ = [PASTE_HANDLER]
