from fastapi import Body, Depends, HTTPException
from fastapi.routing import APIRoute

from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT, decodeJWT
from db import database
from models.models import AdminLogin, Book


def check_admin(jwt: str = Depends(JWTBearer())):
    payload = decodeJWT(jwt)
    if payload.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    return jwt


async def login_admin(user: AdminLogin = Body(...)):
    user = user.model_dump()
    check_user = await database.login_admin(user)
    if check_user and check_user.get('email', False):
        return signJWT(check_user['email'], role='admin')
    else:
        return check_user


async def update_book(id: str, update_dict: dict):
    book = await database.update_book_from_db(id, update_dict)
    if book:
        return book
    else:
        return {"message": "Book not found"}


async def delete_book(id: str):
    result = await database.delete_book_from_db(id)

    if result.deleted_count == 1:
        return {"message": "Book deleted successfully"}
    else:
        return {"message": "Book not found"}


routes = [
    APIRoute(path='/login_admin/', endpoint=login_admin, methods=["POST"]),
    APIRoute(path='/book/{id}/', endpoint=update_book, methods=["PATCH", "PUT"], response_model=Book, dependencies=[Depends(check_admin)]),
    APIRoute(path='/book/{id}/', endpoint=delete_book, methods=["DELETE"], dependencies=[Depends(check_admin)]),
]