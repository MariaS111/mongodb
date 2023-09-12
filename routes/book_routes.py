from fastapi.routing import APIRoute
from auth.auth_handler import decodeJWT
from models.models import Book, User, Shelf
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


async def get_shelf(request: Request) -> dict:
    current_user = decodeJWT(request.headers['authorization'].split()[1])
    curr_user = await database.get_profile(current_user['user_id'])
    id = curr_user['_id']
    shelf = await database.get_shelf(id)
    return shelf


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
    APIRoute(path='/get_shelf/', endpoint=get_shelf, methods=["GET"], response_model=Shelf, dependencies=[Depends(JWTBearer())])
]
