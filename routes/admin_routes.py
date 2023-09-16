from fastapi import Body
from fastapi.routing import APIRoute
from auth.auth_handler import signJWT
from db import database
from models.models import Admin, AdminLogin


async def login_admin(user: AdminLogin = Body(...)):
    user = user.model_dump()
    check_user = await database.login_admin(user)
    if check_user and check_user.get('email', False):
        return signJWT(check_user['email'], role='admin')
    else:
        return check_user


async def update_book():
    pass


async def delete_book():
    pass

routes = [
    APIRoute(path='/login_admin/', endpoint=login_admin, methods=["POST"]),
    APIRoute(path='/book/{id}/', endpoint=update_book, methods=["DELETE"]),
    APIRoute(path='/book/{id}/', endpoint=delete_book, methods=["GET"]),
]