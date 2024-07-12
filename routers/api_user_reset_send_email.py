from fastapi import APIRouter, Request, Form, BackgroundTasks
from fastapi.responses import JSONResponse
from utils.token_verify_creator import token_creator
from utils.datamodel import ResetPasswordEmailRequest
import aiomysql
import yagmail
import os

router = APIRouter()
headers = {"Content-Type": "application/json; charset=utf-8"}

@router.post("/api/user/reset_request")
async def reset_password(request: Request, e:ResetPasswordEmailRequest, bt:BackgroundTasks): 
    try:
        print(e.email)
        async def check_email_send_url(request,email):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute('SELECT * FROM user_info WHERE email = %s;', (email,))
                    user_info = await cursor.fetchone()
                    if user_info:
                        input_data = {"id": user_info['id'],'username':user_info['username'],'email':user_info['email'], 'password':user_info['password']}                                        
                        access_token = token_creator(data=input_data)
                        return access_token

                    else:
                        content_data = {"error": True, "message": "Invalid user email, please input signup user email address."}
                        return JSONResponse(status_code=400, content=content_data, headers=headers)
                    
        def send_email(subject, body, to_email):
            try:
                yag = yagmail.SMTP(os.getenv('PERSONAL_GMAIL'), os.getenv('PERSONAL_GMAIL_PASSWORD'))
                yag.send(
                    to=to_email,
                    subject=subject,
                    contents=body
                )
                print("Email sent successfully")
            except Exception as e:
                print(f"Failed to send email: {e}")
                raise e

        result =  await check_email_send_url(request, e.email)
        if isinstance(result, JSONResponse):
            return result
        access_token =  result
        print('48',os.getenv('PERSONAL_GMAIL'))
        print('49',os.getenv('PERSONAL_GMAIL_PASSWORD'))

        if access_token:
            subject = "[Please Don't Reply to This Address] Reset Taipei-Day-Trip Password"
            body = f"Click the link below to reset your password:\n\nhttps://raphaelfang.com/api/user/reset_url_verify?token={access_token}"
            # bt.add_task(send_email, subject, body, e.email)
            send_email(subject, body, e.email)


            content_data = {"success": True, "message": "The reset password url has send to your email address."}
            return JSONResponse(status_code=200, content=content_data, headers=headers)
        
        content_data = {"success": False, "message": "error occur, sth wrong here."}
        return JSONResponse(status_code=200, content=content_data, headers=headers)
        
    
    except (yagmail.error.YagMailError) as err:
        return JSONResponse(status_code=400, content={"error": True, "message": str(err)}, headers=headers)
    except (aiomysql.Error) as err:
        return JSONResponse(status_code=500,content={"error": True, "message": str(err)},headers=headers)
    except (ValueError, Exception) as err:
        return JSONResponse(status_code=400,content={"error": True, "message": str(err)},headers=headers)