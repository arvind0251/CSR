from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Word"]
word_collection = db["WordDb"]

async def find_responses(word):
    try:
        results = await word_collection.find({"word": word}).to_list(length=10)
        print(f"[DB] Fetched {len(results)} responses for: {word}")
        return results
    except Exception as e:
        print(f"[DB ERROR] find_responses({word}): {e}")
        return []

async def insert_response(trigger, reply, check_type):
    try:
        print(f"[DB] Inserting response: '{trigger}' -> '{reply}' ({check_type})")
        return await word_collection.insert_one({
            "word": trigger,
            "text": reply,
            "check": check_type
        })
    except Exception as e:
        print(f"[DB ERROR] insert_response({trigger}): {e}")
        return None

async def count_words():
    try:
        total = await word_collection.count_documents({})
        print(f"[DB] Total words learned: {total}")
        return total
    except Exception as e:
        print(f"[DB ERROR] count_words: {e}")
        return 0
