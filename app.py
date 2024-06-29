from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils.auth_middleware import AuthMiddleware 
from utils.cors import setup_cors 
from utils.db import pool_buildup
from routers import api_attraction, api_attractions, api_mrts, api_booking_get, api_booking_post, api_booking_delete, api_user_get, api_user_logout, api_user_post, api_user_put
from starlette.responses import RedirectResponse

app=FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
app.add_middleware(AuthMiddleware)
setup_cors(app)

db_pool ={
    "basic_db":pool_buildup(),
}
@app.middleware("http")
async def redirect_http_to_https(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https", netloc=request.url.hostname) # 取消掉8443，但奇怪的是8443也可以正常執行?
        return RedirectResponse(url)
    response = await call_next(request)
    return response

@app.middleware("http")
async def attach_db_connection(request: Request, call_next):
    request.state.db_pool = db_pool
    response = await call_next(request)
    return response

app.include_router(api_mrts.router)
app.include_router(api_attraction.router)
app.include_router(api_attractions.router)

app.include_router(api_user_post.router)
app.include_router(api_user_put.router)
app.include_router(api_user_get.router)
app.include_router(api_user_logout.router)

app.include_router(api_booking_get.router)
app.include_router(api_booking_post.router)
app.include_router(api_booking_delete.router)



# Static Pages (Never Modify Code in this Block)
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