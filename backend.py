# from pymongo import MongoClient
# cluster = MongoClient('mongodb://localhost:27017')
# db = cluster['MongoTest']
# users_collection = db['users']
# books_collection = db['books']
# shelves_collection = db['shelves']


def register(collection, shelves, name, password):
    number_of_users = collection.count_documents({}) + 1
    if name not in collection.distinct('name') and len(password) >= 8:
        collection.insert_one({
            "_id": number_of_users,
            "name": name,
            "password": password,
        })
        create_shelf(shelves, number_of_users)
        return collection.find_one({'name': name})
    else:
        return 'This name is already taken or password is less than 8 characters'


def create_shelf(collection, pk):
    collection.insert_one({
        "_id": pk,
        "shelf": "Your book shelf"
    })


def login(collection, name, password):
    user = collection.find_one({
        'name': name,
        'password': password
    })
    return user


def logout():
    pass


def search(**kwargs):
    pass


def add_book_to_db(collection, title, author, description):
    number_of_books = collection.count_documents({}) + 1
    collection.insert_one({
        "_id": number_of_books,
        "title": title,
        "author": author,
        "description": description
    })


def mark_book_as_read(collection, pk, mark):
    collection.update_one(
        {"_id": pk},
        {"$set": {"status": "read", "mark": mark}})


def add_to_shelf(collection, book_collection, shelf_pk, book_pk):
    book = book_collection.find_one({"_id": book_pk})
    collection.update_one(
        {"_id": shelf_pk},
        {"$push": {"books": book}})
    add_status_to_book(collection, book_pk, shelf_pk)


def add_status_to_book(collection, book_pk, shelf_pk):
    collection.update_one(
        {"_id": shelf_pk},
        {"$set": {str(book_pk): "unread"}})


def show_unread_books_from_shelf(collection):
    collection.find_many({"status": "unread"})


def show_read_books_from_shelf(collection):
    collection.find_many({"status": "read"})