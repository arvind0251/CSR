# handlers/commands.py
from pyrogram import filters
from pyrogram.types import Message
from config import ADMIN_IDS
from db.mongo import count_words

learning_enabled = True

def register_command_handlers(app):
    @app.on_message(filters.command("start"))
    async def start(client, message: Message):
        await message.reply("Hello! I'm a learning bot. Reply to my messages and I'll remember your response!")

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
