from fastapi import APIRouter, Request, BackgroundTasks
from fastapi.responses import RedirectResponse, JSONResponse
from authlib.integrations.starlette_client import OAuth
import secrets
from utils.token_verify_creator import token_creator
import redis
import json
import aiomysql 
import redis.asyncio as aioredis
import os 

router = APIRouter()

oauth = OAuth()
async def init_oauth():
    oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        redirect_uri='https://raphaelfang.com/auth/callback',
        client_kwargs={'scope': 'openid email profile'},

        jwks_uri='https://www.googleapis.com/oauth2/v3/certs',
        access_token_url='https://oauth2.googleapis.com/token',
        authorize_url='https://accounts.google.com/o/oauth2/v2/auth',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo'
    )
    return oauth

@router.get("/auth/login")
async def auth_login(request: Request):
    try:
        oauth = await init_oauth()
        state = secrets.token_urlsafe(16)
        request.session.clear()  # 解決CSRF非同源問題，清除掉之前的cookie
        request.session['state'] = state
        redirect_uri = 'https://raphaelfang.com/auth/callback'  
        return await oauth.google.authorize_redirect(request, redirect_uri, state=state)
    
    except (ValueError, Exception) as err:
        url = "/?status=error&message=" + str(err)
        return RedirectResponse(url=url)


@router.get('/auth/callback')
async def auth_callback(request: Request, bt:BackgroundTasks):
    error = request.query_params.get('error')
    print(error)
    if error == 'access_denied':
        return RedirectResponse( url = "/?status=error&message=Access+Denied") # 好怪，在這邊加上status_code就會報錯，GPT的回復：在处理FastAPI的RedirectResponse时，不能直接在创建响应时设置status_code。RedirectResponse默认使用302重定向状态码。如果要更改状态码，需要在响应对象创建后进行修改。
    
    try:
        oauth = await init_oauth()
        token = await oauth.google.authorize_access_token(request)
        nonce_in_session = request.session.get('nonce')
        user = await oauth.google.parse_id_token(token, nonce=nonce_in_session)

        async def search_user_login(request,sub,email,name,pic):
            sql_pool = request.state.async_sql_pool 
            async with sql_pool.acquire() as connection:
                async with connection.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute("SELECT * FROM user_info WHERE provider_id = %s AND email = %s AND username = %s;", (sub, email, name))
                    data =  await cursor.fetchone()

                    if data:
                        input_data = {"id": data['id'],'username':data['username'],'email':data['email'], 'password':''}                                        
                        access_token = token_creator(data=input_data)
                        await cursor.execute("SELECT * FROM user_booking_tentative WHERE creator_id = %s;", (data['id'],)) 
                        last_d = await cursor.fetchone()

                        # await cursor.execute("SELECT * FROM user_booking_finalized WHERE creator_id = %s AND given_status = 'PAID' ORDER BY created_at LIMIT 10;", (data['id'],))
                        # history_d = await cursor.fetchall()

                        return access_token, last_d
                    else:
                        await cursor.execute("INSERT INTO user_info (provider_id, email, username, auth_provider, profile_picture) VALUES (%s, %s, %s, 'Google', %s)", (sub,email,name,pic)) 
                        await connection.commit()
                        await cursor.execute("SELECT LAST_INSERT_ID();")
                        new_user_id = await cursor.fetchone()       
                        input_data = {"id": new_user_id['LAST_INSERT_ID()'],'username':name,'email':email, 'password':''}                                        
                        access_token = token_creator(data=input_data)
                        last_d = None

                        return access_token, last_d
                        
        async def booking_data_r(request, last_d):
            redis_pool = request.state.async_redis_pool
            async with aioredis.Redis(connection_pool=redis_pool) as r:
                if last_d:
                        booking_data = {
                        "attraction_id": last_d['attraction_id'],
                        "name": last_d['name'],
                        "address": last_d['address'],
                        "image": last_d['image'],
                        "date": last_d['date'].strftime("%Y-%m-%d"),
                        "time": last_d['time'],
                        "price": str(last_d['price'])
                        }
                await r.set(f"user:{last_d['creator_id']}:booking", json.dumps(booking_data))

                # if history_d:
                #     booking_data_history = []
                #     for n in history_d:
                #         con = {"data": {
                #             "number": n['order_number'],
                #             "price": int(n['price']),
                #             "trip": {
                #             "attraction": {
                #                 "id": n['attr_id'],
                #                 "name": n['attr_name'],
                #                 "address": n['attr_address'],
                #                 "image": n['attr_image']
                #             },
                #             "date": n['attr_date'].strftime("%Y-%m-%d"),
                #             "time":n['attr_time']
                #             },
                #             "contact": {
                #             "name": n['contact_name'],
                #             "email": n['contact_email'],
                #             "phone": n['contact_phone']
                #             },
                #             "status": 1 if n['given_status']=='PAID' else 0
                #             }}
                #         booking_data_history.append(con)
                #     await r.set(f"user:{last_d['creator_id']}:booking_history", json.dumps(booking_data_history))

        
        if user: # 原本一直想不到該怎麼傳遞這部份的資訊，畢竟是直接回到主畫面，但是想到可以打資料加到url送回去
            access_token, last_d = await search_user_login(request,user.get('sub'), user.get('email'), user.get('name'), user.get('picture'))
            bt.add_task(booking_data_r, request, last_d)
            response = RedirectResponse(url="/?status=success")
            response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Strict")
            return response
        else:
            response = RedirectResponse(url="/?status=error&message=Missing correct token response from Google")
            return response         

    except (aiomysql.Error, redis.RedisError) as err:
        url = "/?status=error&message=" + str(err)
        return RedirectResponse(url=url)
    except (ValueError, Exception) as err:
        url = "/?status=error&message=" + str(err)
        return RedirectResponse(url=url)

