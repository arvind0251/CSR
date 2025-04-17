import random
import traceback
from pyrogram import filters
from pyrogram.enums import ChatAction
from pyrogram.types import Message
from db.mongo import find_responses, insert_response
from utils.filters import is_clean_text
from handlers.commands import learning_enabled

def register_message_handler(app):
    @app.on_message(filters.text & filters.incoming & ~filters.service)
    async def handle_messages(client, message: Message):
        try:
            print(f"[DEBUG] Received message: {message.text}")
            print(f"[DEBUG] Chat type: {message.chat.type}, From: {message.from_user.id}")
            print(f"[DEBUG] Is reply: {message.reply_to_message is not None}")

            if not is_clean_text(message.text):
                print("[DEBUG] Message rejected by is_clean_text()")
                return

            if message.chat.type in ["private", "group"]:
                await client.send_chat_action(message.chat.id, ChatAction.TYPING)

            if not message.reply_to_message:
                responses = await find_responses(message.text)
                print(f"[DEBUG] Found responses: {responses}")
                if responses:
                    res = random.choice(responses)
                    try:
                        if res["check"] == "sticker":
                            await message.reply_sticker(res["text"])
                        else:
                            await message.reply_text(res["text"])
                    except Exception as inner_err:
                        print(f"[ERROR] While replying (no-reply case): {inner_err}")
                        traceback.print_exc()
            else:
                reply = message.reply_to_message
                me = await client.get_me()
                if reply.from_user.id == me.id:
                    responses = await find_responses(message.text)
                    print(f"[DEBUG] Replying to bot — found: {responses}")
                    if responses:
                        res = random.choice(responses)
                        try:
                            if res["check"] == "sticker":
                                await message.reply_sticker(res["text"])
                            else:
                                await message.reply_text(res["text"])
                        except Exception as inner_err:
                            print(f"[ERROR] While replying to bot: {inner_err}")
                            traceback.print_exc()
                elif learning_enabled:
                    print("[DEBUG] Learning enabled. Saving user reply.")
                    if message.text:
                        await insert_response(reply.text, message.text, "text")
                    elif message.sticker:
                        await insert_response(reply.text, message.sticker.file_id, "sticker")

        except Exception as e:
            print("[FATAL ERROR] in handle_messages():")
            traceback.print_exc()
