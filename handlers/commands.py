# handlers/commands.py
from pyrogram import filters
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from config import ADMIN_IDS
from db.mongo import count_words

learning_enabled = True

def register_command_handlers(app):
    @app.on_message(filters.command("start"))
    async def start(client, message: Message):
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Rudra", url="https://t.me/RU_DRA_65")],
                [InlineKeyboardButton("Join Group", url="https://t.me/RU_DRA_098")]  # replace this
            ]
        )

        await message.reply_photo(
            photo="https://files.catbox.moe/xniwk3.jpg",  # replace with your image URL
            caption="**Hey! I'm a learning bot.**\n\nReply to my messages and I’ll remember your responses!",
            reply_markup=keyboard
        )

    @app.on_message(filters.command("help"))
    async def help_cmd(client, message: Message):
        await message.reply("Just send me a message. If you reply to me, I’ll learn from it.")

    @app.on_message(filters.command("stats"))
    async def stats(client, message: Message):
        total = await count_words()
        await message.reply(f"I have learned **{total}** responses.")

    @app.on_message(filters.command("togglelearn"))
    async def toggle_learning(client, message: Message):
        global learning_enabled
        if message.from_user.id not in ADMIN_IDS:
            return await message.reply("Only admins can toggle learning mode.")
        learning_enabled = not learning_enabled
        await message.reply(f"Learning mode is now {'enabled' if learning_enabled else 'disabled'}.")

    return learning_enabled
