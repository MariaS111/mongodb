import backend
from context_manager import MongoDBConnection

if __name__ == '__main__':
    uri = "mongodb://localhost:27017/"
    with MongoDBConnection(uri) as client:
        db = client['MongoTest']
        users_collection = db['users']
        books_collection = db['books']
        shelves_collection = db['shelves']
        backend.add_to_shelf(shelves_collection, books_collection, 1, 1)
