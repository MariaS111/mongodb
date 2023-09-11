from fastapi.routing import APIRoute
from fastapi import Body, Depends
from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT, decodeJWT
from models.models import User, UserLogin
from db import database


async def login_user(user: UserLogin = Body(...)):
    user = user.model_dump()
    check_user = await database.login(user)
    if check_user and check_user.get('email', False):
        return signJWT(check_user['email'])
    else:
        return check_user


async def get_profile(current_user: User = Depends(decodeJWT)):
    curr_user = await database.get_profile(current_user['user_id'])
    return {'name': curr_user['name'], 'email': curr_user['email']}


async def sign_up_user(user: User = Body(...)):
    user = user.model_dump()
    user_new = await database.register(user)
    if user_new.get('email', False):
        return signJWT(user_new['email'])
    else:
        return user_new


routes = [
    APIRoute(path='/login_user/', endpoint=login_user, methods=["POST"]),
    APIRoute(path='/sign_up/', endpoint=sign_up_user, methods=["POST"]),
    APIRoute(path='/profile/', endpoint=get_profile, methods=["GET"], dependencies=[Depends(JWTBearer())]),
]
