from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from routers import api_at_mrts, api_attraction, api_attractions, api_booking_post, api_booking_delete, api_booking_get, api_user_get, api_user_google, api_user_logout, api_user_post, api_user_put, api_orders_post,api_order_get,api_orders_all,api_user_reset_send_email,api_user_reset_url,api_user_reset_password
from utils.cors import setup_cors 
from utils.auth_middleware import AuthMiddleware 
from utils.db.sql import  build_async_sql_pool
from utils.db.redis import  build_async_redis_pool
from starlette.middleware.sessions import SessionMiddleware
import os
from utils.ttl import handle_expired_keys
import asyncio

app=FastAPI(docs_url="/tdt/v1/docs")
app.mount("/tdt/v1/static", StaticFiles(directory='static'), name="static")
app.add_middleware(AuthMiddleware)
setup_cors(app)

# !-----------------------------------------
@app.on_event("startup")
async def startup_event():
    app.state.async_sql_pool = await build_async_sql_pool()
    app.state.async_redis_pool = await build_async_redis_pool()
	
    app.state.handle_expired_keys_task = asyncio.create_task(handle_expired_keys(app.state.async_redis_pool, app.state.async_sql_pool))  # 開啟ttl 監聽

@app.on_event("shutdown")  
async def shutdown_event():
	app.state.handle_expired_keys_task.cancel() 
	await app.state.handle_expired_keys_task
	
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

# !-----------------------------------------
app.include_router(api_at_mrts.router, tags=["attraction"], prefix="/tdt/v1")
app.include_router(api_attraction.router, tags=["attraction"], prefix="/tdt/v1")
app.include_router(api_attractions.router, tags=["attraction"], prefix="/tdt/v1")

app.include_router(api_user_post.router, tags=["user"], prefix="/tdt/v1")
app.include_router(api_user_put.router, tags=["user"], prefix="/tdt/v1")
app.include_router(api_user_get.router, tags=["user"], prefix="/tdt/v1")
app.include_router(api_user_logout.router, tags=["user"], prefix="/tdt/v1")
app.include_router(api_user_google.router, tags=["user"], prefix="/tdt/v1")

app.include_router(api_booking_post.router, tags=["booking"], prefix="/tdt/v1")
app.include_router(api_booking_get.router, tags=["booking"], prefix="/tdt/v1")
app.include_router(api_booking_delete.router, tags=["booking"], prefix="/tdt/v1")

app.include_router(api_orders_post.router, tags=["order"], prefix="/tdt/v1")
app.include_router(api_order_get.router, tags=["order"], prefix="/tdt/v1")
app.include_router(api_orders_all.router, tags=["order"], prefix="/tdt/v1")

app.include_router(api_user_reset_password.router, tags=["reset_password"], prefix="/tdt/v1")
app.include_router(api_user_reset_send_email.router, tags=["reset_password"], prefix="/tdt/v1")
app.include_router(api_user_reset_url.router, tags=["reset_password"], prefix="/tdt/v1")


# !-----------------------------------------
html_router = APIRouter(prefix="/tdt/v1")

@html_router.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@html_router.get("/attraction/{id}", include_in_schema=False)
async def api_attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@html_router.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@html_router.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")
@html_router.get("/history_orders", include_in_schema=False)
async def history_orders(request: Request):
	return FileResponse("./static/history_orders.html", media_type="text/html")

app.include_router(html_router)