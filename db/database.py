from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config


URI = config("MONGODB_URL", default="mongodb://localhost:27017/")
CLIENT = AsyncIOMotorClient(URI)
DB = CLIENT['MongoTest']


def get_books_from_db():
    cursor = DB['books'].find({})
    return cursor


def get_book_from_db(id):
    cursor = DB['books'].find_one({"_id": ObjectId(id)})
    return cursor


def create_book(book):
    DB['books'].insert_one(book)


async def register(user_data):
    existing_user = await DB['users'].find_one({'email': user_data['email']})
    if existing_user:
        return {'detail': 'User with this email already exists'}
    else:
        result = await DB['users'].insert_one(user_data)
        print(result)
        user_new = await DB['users'].find_one({'_id': result.inserted_id})
        return user_new


def login(user_data):
    user = DB['users'].find_one(user_data)
    if user:
        return user
    else:
        return {'detail': 'User with this credentials doesn\'t exist'}
