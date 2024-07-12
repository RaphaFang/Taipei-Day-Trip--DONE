from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_verifier
from datetime import timedelta
from utils.datamodel import ResetPasswordNewPassword
import aiomysql

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.put("/api/user/reset_password")
async def reset_password(request: Request, raw_new_p:ResetPasswordNewPassword): 
            # 前端檢測這串url代碼，如果是success，才可以跳出修改密碼的彈窗
            # 前端檢測cookie，如果有才可以讓他修改，並且這cookie的期限很短
    try:
        token = request.cookies.get("access_token")
        token_response = token_verifier(token)
        if isinstance(token_response, JSONResponse):
            return token_response
        token_output = token_response

        print('22',token_output)

        async def set_new_password(request, new_p, id, name, email):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(
                        'UPDATE user_info SET password = %s WHERE id = %s AND username = %s AND email = %s;', 
                        (new_p, id, name, email)
                    )
                    await connection.commit()
                    if cursor.rowcount == 0:
                        return {"status": False, "message": "Password updated failed, please retry the url link from your email."}
                    return {"status": True, "message": "Password updated successfully."}

        if token_output: # 這邊需要把東西放到 add_task嗎？ 要想想
            result = await set_new_password(request, raw_new_p.password, token_output['id'], token_output['username'], token_output['email'])
            print('39',result)
            if result['status'] == True:
                response = JSONResponse(status_code=200, content={f"message": {result['message']}})
            else:
                response = JSONResponse(status_code=400, content={f"message": {result['message']}})
            response.delete_cookie(key="access_token")
            return response

    except (aiomysql.Error) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)