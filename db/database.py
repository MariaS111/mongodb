from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config


URI = config("MONGODB_DOCKER_URL", default="mongodb://localhost:27017/")
CLIENT = AsyncIOMotorClient(URI)
DB = CLIENT['MongoTest']


async def get_books_from_db():
    cursor = DB['books'].find({})
    return cursor


async def get_book_from_db(id):
    cursor = await DB['books'].find_one({"_id": ObjectId(id)})
    return cursor


async def update_book_from_db(id, update_dict):
    await DB['books'].update_one({"_id": ObjectId(id)}, {'$set': update_dict})
    cursor = await DB['books'].find_one({"_id": ObjectId(id)})
    return cursor


async def delete_book_from_db(id):
    result = await DB['books'].delete_one({"_id": ObjectId(id)})
    return result


async def create_book(book):
    book = await DB['books'].insert_one(book)
    return book


async def create_shelf(shelf_json):
    result = await DB['shelves'].insert_one(shelf_json)
    return result


async def get_shelf(id):
    result = await DB['shelves'].find_one({'_id': id})
    return result


async def register(user_data):
    existing_user = await DB['users'].find_one({'email': user_data['email']})
    if existing_user:
        return {'detail': 'User with this email already exists'}
    else:
        result = await DB['users'].insert_one(user_data)
        shelf_json = {'_id': result.inserted_id, 'books': []}
        await create_shelf(shelf_json)
        user_new = await DB['users'].find_one({'_id': result.inserted_id})
        return user_new


async def mark_as_read(shelf_id, updated_shelf):
    await DB['shelves'].update_one({"_id": shelf_id}, {"$set": updated_shelf})


async def login(user_data):
    user = await DB['users'].find_one(user_data)
    if user:
        return user
    else:
        return {'detail': 'User with this credentials doesn\'t exist'}


async def login_admin(user_data):
    user = await DB['admins'].find_one(user_data)
    if user:
        return user
    else:
        return {'detail': 'Admin with this credentials doesn\'t exist'}


async def get_profile(email):
    user = await DB['users'].find_one({'email': email})
    if user:
        return user
    else:
        return {'detail': 'User with this credentials doesn\'t exist'}


async def add_book_to_shelf(shelf_id, book):
    res = await DB['shelves'].update_one(
        {'_id': shelf_id},
        {'$push': {'books': book}}
    )
    if res:
        return {'message': "Success"}

