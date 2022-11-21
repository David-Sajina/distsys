import aiohttp
import aiosqlite
import asyncio
import time
from aiohttp import web
tasks = []
routes = web.RouteTableDef()
"""ime prezime grad email"""
@routes.post("/filterUser")
async def get_nes(request):
    req = await request.json()
    temp = req
    temp = temp.get("results")
    temp = temp[0].get("name")
    tasks.append({"ime": temp.get("first"),"prezime":temp.get("last")})
    temp = req.get("results")
    tasks.append({"city": temp[0].get("city"),"email":temp[0].get("email")})
    temp = []

    print("person", tasks)
    return web.json_response({"Status": "ok","message":req}, status=200)


app = web.Application()

app.router.add_routes(routes)

web.run_app(app, port=8082)