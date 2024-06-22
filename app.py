from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from utils.auth_middleware import AuthMiddleware 
from utils.cors import setup_cors 
from utils.db import pool_buildup
from routers import api_attraction, api_attractions, api_mrts, api_user, api_user_auth_put, api_user_auth_get
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
app.include_router(api_user.router)
app.include_router(api_user_auth_put.router)
app.include_router(api_user_auth_get.router)


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

# uvicorn app:app --reload
# cd /Users/fangsiyu/Desktop/taipei-day-trip
# nano ~/.zshrc
# source ~/.zshrc