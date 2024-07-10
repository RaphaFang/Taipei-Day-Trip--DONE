from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import api_at_mrts, api_attraction, api_attractions, api_booking_post, api_booking_delete, api_booking_get, api_user_get, api_user_google, api_user_logout, api_user_post, api_user_put, api_orders_post,api_order_get,api_orders_all
from utils.cors import setup_cors 
from utils.auth_middleware import AuthMiddleware 
from utils.db.sql import  build_async_sql_pool
from utils.db.redis import  build_async_redis_pool
from starlette.middleware.sessions import SessionMiddleware
import os

app=FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
app.add_middleware(AuthMiddleware)
setup_cors(app)

# !-----------------------------------------
@app.on_event("startup")
async def startup_event():
    app.state.async_sql_pool = await build_async_sql_pool()
    app.state.async_redis_pool = await build_async_redis_pool()

@app.on_event("shutdown")
async def shutdown_event():
    app.state.async_sql_pool.close()
    await app.state.async_sql_pool.wait_closed()
    await app.state.async_redis_pool.disconnect()

@app.middleware("http")
async def all_db_connection(request: Request, call_next):
    request.state.async_sql_pool = app.state.async_sql_pool
    request.state.async_redis_pool = app.state.async_redis_pool
    response = await call_next(request)
    return response

GOOGLE_SESSION_SECRET_KEY= os.getenv('GOOGLE_SESSION_SECRET_KEY')
app.add_middleware(SessionMiddleware, secret_key=GOOGLE_SESSION_SECRET_KEY, same_site="lax", https_only=False)
# app.include_router(auth_google_login.router)

# !-----------------------------------------
app.include_router(api_at_mrts.router)
app.include_router(api_attraction.router)
app.include_router(api_attractions.router)
app.include_router(api_user_post.router)
app.include_router(api_user_put.router)
app.include_router(api_user_get.router)
app.include_router(api_user_logout.router)
app.include_router(api_booking_post.router)
app.include_router(api_booking_get.router)
app.include_router(api_booking_delete.router)
app.include_router(api_orders_post.router)
app.include_router(api_order_get.router)
app.include_router(api_user_google.router)

app.include_router(api_orders_all.router)


@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def api_attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# uvicorn app:app --host 127.0.0.1 --port 8000 --ssl-keyfile /Users/fangsiyu/Desktop/secrets/privkey.pem --ssl-certfile /Users/fangsiyu/Desktop/secrets/fullchain.pem --reload
# cd /Users/fangsiyu/Desktop/taipei-day-trip
# nano ~/.zshrc
# source ~/.zshrc
