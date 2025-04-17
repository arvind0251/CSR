# db/mongo.py
from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo_client = AsyncIOMotorClient(MONGO_URL)
db = mongo_client["Word"]
word_collection = db["WordDb"]

async def find_responses(word):
    return await word_collection.find({"word": word}).to_list(length=10)

async def insert_response(trigger, reply, check_type):
    return await word_collection.insert_one({"word": trigger, "text": reply, "check": check_type})

async def count_words():
    return await word_collection.count_documents({})
