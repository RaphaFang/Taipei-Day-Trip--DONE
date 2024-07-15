from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
import redis.asyncio as aioredis 
import redis

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.delete("/api/booking")
async def api_booking_delete(request: Request, bt:BackgroundTasks): 
    try:
        token = request.cookies.get("access_token")
        token_response = token_verifier(token)
        if isinstance(token_response, JSONResponse):
            return token_response
        token_output = token_response

        if token_output:
            async def delete_user_r(request, id):
                redis_pool = request.state.async_redis_pool
                async with aioredis.Redis(connection_pool=redis_pool) as r:
                    await r.delete(f"user:{id}:booking")
            bt.add_task(delete_user_r, request, token_output['id'])

            content_data = {"ok": True}
            return JSONResponse(content=content_data, headers=headers)           

    except (redis.RedisError) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)