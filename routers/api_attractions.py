from fastapi import APIRouter, Request, Query
from fastapi.responses import JSONResponse
import aiomysql 
import json
from typing import Optional

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.get("/api/attractions")
async def api_attractions(request: Request, page: int=Query(..., ge=0), keyword: Optional[str] = None):
    try:
        offset_num = page*12
        keyword_format = f"%{keyword}%" 

        async def search_attr_keyword(request,keyword,offset_num,keyword_format):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    if keyword==None:
                        await cursor.execute("SELECT  * FROM processed_data LIMIT 12 OFFSET %s;", (offset_num,)) 
                        attract_data = await cursor.fetchall()
                        await cursor.execute("SELECT COUNT(*) AS t FROM processed_data;") 
                    else:
                        await cursor.execute("SELECT  * FROM processed_data WHERE mrt LIKE %s OR name LIKE %s LIMIT 12 OFFSET %s;", (keyword_format, keyword_format, offset_num,)) 
                        attract_data = await cursor.fetchall()
                        await cursor.execute("SELECT COUNT(*) AS t FROM processed_data WHERE mrt LIKE %s OR name LIKE %s;", (keyword_format, keyword_format))
                    sum_rows = await cursor.fetchone()
                    
                    next_page = page+1 if sum_rows['t'] > (page+1)*12 else None
                    each_data_list = [{'id':each['id'],"name":each["name"],'category':each['category'], 'description':each['description'],'address':each['address'],'transport':each['transport'],'mrt':each['mrt'],'lat':each['lat'],'lng':each['lng'], 'images':json.loads(each['images'])} for each in attract_data]
                    return {"data": each_data_list, "nextPage":next_page}
        result = await search_attr_keyword(request,keyword,offset_num,keyword_format)
        return JSONResponse(content=result, headers=headers)

    except aiomysql.Error as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (KeyError,ValueError) as err:
        return JSONResponse(status_code=400, content={"error": True, "message":{str(err)}}, headers=headers)
    except (Exception) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)