# handlers/message_handler.py
import random
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message
from db.mongo import find_responses, insert_response
from utils.filters import is_clean_text
from handlers.commands import learning_enabled

def register_message_handler(app):
    @app.on_message(filters.text & ~filters.bot)
    async def handle_messages(client, message: Message):
        if not is_clean_text(message.text):
            return

        if message.chat.type in ["private", "group"]:
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if not message.reply_to_message:
            responses = await find_responses(message.text)
            if responses:
                res = random.choice(responses)
                try:
                    if res["check"] == "sticker":
                        await message.reply_sticker(res["text"])
                    else:
                        await message.reply_text(res["text"])
                except Exception:
                    pass
        else:
            reply = message.reply_to_message
            me = await client.get_me()
            if reply.from_user.id == me.id:
                responses = await find_responses(message.text)
                if responses:
                    res = random.choice(responses)
                    try:
                        if res["check"] == "sticker":
                            await message.reply_sticker(res["text"])
                        else:
                            await message.reply_text(res["text"])
                    except Exception:
                        pass
            elif learning_enabled:
                if message.text:
                    await insert_response(reply.text, message.text, "text")
                elif message.sticker:
                    await insert_response(reply.text, message.sticker.file_id, "sticker")
