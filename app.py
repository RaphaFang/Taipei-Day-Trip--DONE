from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers.auth_middleware import AuthMiddleware 
from routers.cors import setup_cors 
from routers import attractions, mrts, attraction, api_user, api_user_auth_put, api_user_auth_get
from db import pool_buildup

app=FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
app.add_middleware(AuthMiddleware)
setup_cors(app)

db_pool ={
    "basic_db":pool_buildup(),
}
@app.middleware("http")
async def attach_db_connection(request: Request, call_next):
    request.state.db_pool = db_pool
    response = await call_next(request)
    return response


app.include_router(mrts.router)
app.include_router(attraction.router)
app.include_router(attractions.router)
app.include_router(api_user.router)
app.include_router(api_user_auth_put.router)
app.include_router(api_user_auth_get.router)


# Static Pages (Never Modify Code in this Block)
@app.get("/", include_in_schema=False)
async def index(request: Request):
	return FileResponse("./static/index.html", media_type="text/html")
@app.get("/attraction/{id}", include_in_schema=False)
async def attraction(request: Request, id: int):
	return FileResponse("./static/attraction.html", media_type="text/html")
@app.get("/booking", include_in_schema=False)
async def booking(request: Request):
	return FileResponse("./static/booking.html", media_type="text/html")
@app.get("/thankyou", include_in_schema=False)
async def thankyou(request: Request):
	return FileResponse("./static/thankyou.html", media_type="text/html")

# uvicorn app:app --reload
# cd /Users/fangsiyu/Desktop/taipei-day-trip

