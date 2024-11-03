from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import aiomysql 
import json

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/attraction/{id}")  
async def api_attractions(request: Request, id=int): 
    try:
        async def search_attr_id(request,id):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("SELECT * FROM processed_data WHERE id = %s", (id,)) 
                    return await cursor.fetchone()  
        result = await search_attr_id(request,id)

        if result:
            result['images'] = json.loads(result['images'])
            return JSONResponse(content={"data": result},headers=headers)
        else:
            con = {"error": True, "message": "inserted id out of range, valid id start from 1 to 58"}
            return JSONResponse(status_code=400,content=con,headers=headers)

    except aiomysql.Error as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (KeyError,ValueError) as err:
        return JSONResponse(status_code=400, content={"error": True, "message":{str(err)}}, headers=headers)
    except (Exception) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)