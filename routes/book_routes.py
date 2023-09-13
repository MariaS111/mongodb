from datetime import datetime
from bson import ObjectId
from fastapi.routing import APIRoute
from auth.auth_handler import decodeJWT
from models.models import Book, User, Shelf, BookEntry, StatusEnum
from db import database
from fastapi import Depends, Request
from auth.auth_bearer import JWTBearer


async def get_books() -> list:
    res = []
    cursor = await database.get_books_from_db()
    for document in await cursor.to_list(length=100):
        document["_id"] = str(document["_id"])
        res.append(document)
    return res


async def get_book(id: str) -> dict:
    book = await database.get_book_from_db(id)
    if book:
        book["_id"] = str(book["_id"])
        return book
    else:
        return {"message": "Book not found"}


async def get_user_id(request: Request) -> dict:
    current_user = decodeJWT(request.headers['authorization'].split()[1])
    curr_user = await database.get_profile(current_user['user_id'])
    return curr_user['_id']


async def get_shelf(request: Request) -> dict:
    id = await get_user_id(request)
    shelf = await database.get_shelf(id)
    for book_entry in shelf.get('books', []):
        book_id = book_entry.get('_id')
        if book_id:
            book_info = await database.get_book_from_db(book_id)
            if book_info:
                book_entry['title'] = book_info['title']
                book_entry['author'] = book_info['author']
                book_entry['description'] = book_info['description']
    return shelf


async def add_book_to_shelf(id: str, request: Request) -> dict:
    shelf_id = await get_user_id(request)
    current_time = datetime.now()
    book = {
        "_id": ObjectId(id),
        "status": StatusEnum.unread,
        "mark": None,
        "timestamp": current_time
    }
    response = await database.add_book_to_shelf(shelf_id, book)
    return response


async def post_book(book: Book) -> dict:
    try:
        book = book.model_dump()
        await database.create_book(book)
    except Exception as e:
        print(e)
    return book


routes = [
    APIRoute(path="/book/", endpoint=get_books, methods=["GET"], response_model=list[Book], dependencies=[Depends(JWTBearer())]),
    APIRoute(path="/book/{id}/", endpoint=get_book, methods=["GET"], response_model=Book, dependencies=[Depends(JWTBearer())]),
    APIRoute(path='/add_book/', endpoint=post_book, methods=["POST"], response_model=Book, dependencies=[Depends(JWTBearer())]),
    APIRoute(path='/get_shelf/', endpoint=get_shelf, methods=["GET"], response_model=Shelf, dependencies=[Depends(JWTBearer())]),
    APIRoute(path="/book/{id}/add_to_shelf/", endpoint=add_book_to_shelf, methods=["PUT", "PATCH"], dependencies=[Depends(JWTBearer())]),
]
