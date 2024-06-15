from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routers.auth_middleware import AuthMiddleware 
from routers.cors import setup_cors 
from routers import attractions, mrts, attraction


app=FastAPI()
app.mount("/static", StaticFiles(directory='static'), name="static")
app.add_middleware(AuthMiddleware)
setup_cors(app)

app.include_router(mrts.router)
app.include_router(attraction.router)
app.include_router(attractions.router)


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
# cd /Users/fangsiyu/Desktop/wehelp/RaphaFang.github.io/part2