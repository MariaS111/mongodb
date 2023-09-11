from fastapi.routing import APIRoute
from models.models import Book
from db import database
from fastapi import Depends
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
        book['_id'] = str(book['_id'])
        return book
    else:
        return {"message": "Book not found"}


async def post_book(book: Book) -> dict:
    try:
        book = book.model_dump()
        await database.create_book(book)
    except Exception as e:
        print(e)
    return {"message": "Success"}


routes = [
    APIRoute(path="/book/", endpoint=get_books, methods=["GET"], dependencies=[Depends(JWTBearer())]),
    APIRoute(path="/book/{id}/", endpoint=get_book, methods=["GET"], dependencies=[Depends(JWTBearer())]),
    APIRoute(path='/add_book/', endpoint=post_book, methods=["POST"], dependencies=[Depends(JWTBearer())])
]
