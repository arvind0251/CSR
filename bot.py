from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from handlers.commands import register_command_handlers
from handlers.message_handler import register_message_handler
from utils.error_handler import setup_global_exception_logger  # NEW LINE

# Setup global error logging
setup_global_exception_logger()  # NEW LINE

app = Client("LearningBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

register_command_handlers(app)
register_message_handler(app)

print("Bot is running...")
app.run()
