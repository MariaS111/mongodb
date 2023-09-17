import uvicorn
from fastapi import APIRouter, FastAPI
from routes import book_routes, user_routes, admin_routes


app = FastAPI()
all_routes = book_routes.routes + user_routes.routes + admin_routes.routes
app.include_router(APIRouter(routes=all_routes))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
