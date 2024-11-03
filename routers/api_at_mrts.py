from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import aiomysql 

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/mrts")
async def api_mrts(request: Request):
    try:
        async def search_mrts(request):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    await cursor.execute("SELECT mrt, COUNT(DISTINCT name) as count FROM processed_data WHERE mrt IS NOT NULL AND mrt != '' GROUP BY mrt ORDER BY count DESC;") 
                    mrts_counted = await cursor.fetchall()
                    return {"data":[n[0] for n in mrts_counted]}
        result = await search_mrts(request)
        return JSONResponse(status_code=200,content=result, headers=headers)

    except aiomysql.Error as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (Exception) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)